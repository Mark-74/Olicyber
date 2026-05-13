# glibc 2.42 IO Structure Reference

All offsets and sizes assume **64-bit Linux** (`__WORDSIZE == 64`, pointer = 8 bytes, `int` = 4 bytes, `long`/`size_t` = 8 bytes, `__off_t` = `__off64_t` = 8 bytes, `wchar_t` = 4 bytes).

---

## `struct _IO_jump_t`

The vtable for an `_IO_FILE`. All fields are function pointers (8 bytes each on 64-bit) produced by the `JUMP_FIELD` macro.

| Offset | Size | Field | Purpose |
|-------:|-----:|-------|---------|
| 0x00 | 8 | `__dummy` | Padding/unused slot (historical, kept for ABI). |
| 0x08 | 8 | `__dummy2` | Padding/unused slot. |
| 0x10 | 8 | `__finish` | Called when the stream is closed/destroyed; releases resources. |
| 0x18 | 8 | `__overflow` | Called when the put-area is full and more output needs to be flushed/buffered. |
| 0x20 | 8 | `__underflow` | Called when the get-area is empty and more input must be fetched. |
| 0x28 | 8 | `__uflow` | Like `__underflow` but also advances the read pointer (returns one character). |
| 0x30 | 8 | `__pbackfail` | Called when `ungetc` cannot put a character back into the buffer. |
| 0x38 | 8 | `__xsputn` | Bulk write: write N bytes to the stream. |
| 0x40 | 8 | `__xsgetn` | Bulk read: read N bytes from the stream. |
| 0x48 | 8 | `__seekoff` | Seek by offset. |
| 0x50 | 8 | `__seekpos` | Seek to absolute position. |
| 0x58 | 8 | `__setbuf` | Install/replace the stream buffer. |
| 0x60 | 8 | `__sync` | Synchronize the stream with the underlying file. |
| 0x68 | 8 | `__doallocate` | Allocate the stream's buffer (called when no buffer is yet attached). |
| 0x70 | 8 | `__read` | Low-level read syscall wrapper. |
| 0x78 | 8 | `__write` | Low-level write syscall wrapper. |
| 0x80 | 8 | `__seek` | Low-level seek syscall wrapper. |
| 0x88 | 8 | `__close` | Low-level close syscall wrapper. |
| 0x90 | 8 | `__stat` | Low-level stat syscall wrapper. |
| 0x98 | 8 | `__showmanyc` | Returns how many characters can be read without blocking. |
| 0xa0 | 8 | `__imbue` | Sets the stream's locale. |

**Total size: `21 * 8 = 0xa8` (168 bytes).**

---

## `struct _IO_FILE`

The public FILE structure. On modern glibc, `_IO_USE_OLD_IO_FILE` is **not** defined, so `_IO_FILE` is the prefix of the wider runtime FILE — its fields don't terminate the struct, they continue into the wide-character/threading bookkeeping fields that follow.

| Offset | Size | Field | Purpose |
|-------:|-----:|-------|---------|
| 0x00 | 4 | `_flags` | High word is `_IO_MAGIC` (`0xFBAD0000`); low bits are flags (`_IO_NO_WRITES`, `_IO_CURRENTLY_PUTTING`, etc.). |
| 0x04 | 4 | *(padding)* | Alignment padding before the next 8-byte pointer. |
| 0x08 | 8 | `_IO_read_ptr` | Current read pointer in the get area. |
| 0x10 | 8 | `_IO_read_end` | End of the get area. |
| 0x18 | 8 | `_IO_read_base` | Start of the get+putback area. |
| 0x20 | 8 | `_IO_write_base` | Start of the put area. |
| 0x28 | 8 | `_IO_write_ptr` | Current put pointer. |
| 0x30 | 8 | `_IO_write_end` | End of the put area. |
| 0x38 | 8 | `_IO_buf_base` | Start of the underlying reserve buffer. |
| 0x40 | 8 | `_IO_buf_end` | End of the underlying reserve buffer. |
| 0x48 | 8 | `_IO_save_base` | Start of saved (non-current) get area, for backup. |
| 0x50 | 8 | `_IO_backup_base` | First valid character of the backup area. |
| 0x58 | 8 | `_IO_save_end` | End of saved get area. |
| 0x60 | 8 | `_markers` | Linked list of `_IO_marker` positions in the stream. |
| 0x68 | 8 | `_chain` | Pointer to the next FILE in the global linked list of open streams. |
| 0x70 | 4 | `_fileno` | Underlying file descriptor. |
| 0x74 | 3 | `_flags2` (bitfield, 24 bits) | Additional internal flags. |
| 0x77 | 1 | `_short_backupbuf[1]` | One-byte fallback backup buffer when malloc fails. |
| 0x78 | 8 | `_old_offset` (`__off_t`) | Legacy 32-bit-era offset field. |
| 0x80 | 2 | `_cur_column` | 1 + column of `pbase()`, or 0 if unknown. |
| 0x82 | 1 | `_vtable_offset` | Vtable offset adjustment (used for multiple-inheritance-style streams). |
| 0x83 | 1 | `_shortbuf[1]` | One-byte fallback buffer. |
| 0x84 | 4 | *(padding)* | Alignment padding before the next 8-byte pointer. |
| 0x88 | 8 | `_lock` | Pointer to the stream's recursive mutex (`_IO_lock_t *`). |

**Size of the `_IO_FILE` prefix: `0x90` (144 bytes).**

Notes on the bitfield row at 0x74: C packs `int _flags2:24` plus `char _short_backupbuf[1]` into the 4 bytes between `_fileno` and `_old_offset`. The bitfield occupies 3 bytes; the `char` array fills the 4th. The next field (`_old_offset`, an 8-byte aligned type) then forces alignment to 0x78.

---

## `struct _IO_FILE_plus`

The actual type of `_IO_2_1_stdin_`, `_IO_2_1_stdout_`, and `_IO_2_1_stderr_`. It wraps a runtime FILE and appends the vtable pointer that all `_IO_*` dispatches go through.

```c
struct _IO_FILE_plus {
    FILE file;                       // runtime FILE (extends _IO_FILE)
    const struct _IO_jump_t *vtable;
};
```

The embedded `file` is the full runtime FILE, not just the `_IO_FILE` prefix shown above — it continues past offset 0x90 with the wide-character and threading bookkeeping (`_offset`, `_codecvt`, `_wide_data`, `_freeres_list`, `_freeres_buf`, `_prevchain`, `_mode`, `_unused3`, `_total_written`, and a small tail padding `_unused2`). On 64-bit glibc 2.42 that runtime FILE is `0xd8` bytes; only the fields relevant to FSOP are listed here.

| Offset | Size | Field | Purpose |
|-------:|-----:|-------|---------|
| 0x00 | 0x90 | *(embedded `_IO_FILE` prefix)* | All fields from the `_IO_FILE` table above, `_flags` through `_lock`. |
| 0x90 | 8 | `_offset` (`__off64_t`) | Current 64-bit file offset. |
| 0x98 | 8 | `_codecvt` | Pointer to the `_IO_codecvt` conversion descriptor for wide I/O. |
| 0xa0 | 8 | `_wide_data` | Pointer to the associated `_IO_wide_data` (wide-character mirror of the byte buffers). |
| 0xa8 | 8 | `_freeres_list` | Pointer used by `__libc_freeres` to release the stream at process exit. |
| 0xb0 | 8 | `_freeres_buf` | Buffer pointer for `__libc_freeres` cleanup. |
| 0xb8 | 8 | `_prevchain` | Back-pointer used to maintain the global FILE chain. |
| 0xc0 | 4 | `_mode` | Stream orientation: negative = byte, positive = wide, 0 = unset. |
| 0xc4 | 4 | `_unused3` | Padding present only on 64-bit (`__WORDSIZE == 64`). |
| 0xc8 | 8 | `_total_written` (`__uint64_t`) | Running total of bytes written. |
| 0xd0 | 8 | `_unused2[8]` | Tail padding (see calculation below). |
| 0xd8 | 8 | `vtable` | Pointer to the `_IO_jump_t` used for all dispatches on this stream. |

**Tail padding calculation.** The source declares:

```c
char _unused2[12 * sizeof(int) - 5 * sizeof(void *)];
```

With `sizeof(int) = 4` and `sizeof(void *) = 8`: `12*4 - 5*8 = 48 - 40 = 8`. So `_unused2` is **8 bytes**, spanning `0xd0..0xd8`.

**Total size: `0xe0` (224 bytes).** This is the size of `_IO_2_1_stdout_`, `_IO_2_1_stderr_`, and `_IO_2_1_stdin_`.

---

## `struct _IO_wide_data`

The wide-character analogue of the byte buffers in `_IO_FILE`, plus its own codecvt copy and a separate vtable pointer.

All `wchar_t *` pointers are 8 bytes (pointers); `wchar_t` itself is 4 bytes on Linux.

| Offset | Size | Field | Purpose |
|-------:|-----:|-------|---------|
| 0x00 | 8 | `_IO_read_ptr` | Current wide read pointer. |
| 0x08 | 8 | `_IO_read_end` | End of wide get area. |
| 0x10 | 8 | `_IO_read_base` | Start of wide get+putback area. |
| 0x18 | 8 | `_IO_write_base` | Start of wide put area. |
| 0x20 | 8 | `_IO_write_ptr` | Current wide put pointer. |
| 0x28 | 8 | `_IO_write_end` | End of wide put area. |
| 0x30 | 8 | `_IO_buf_base` | Start of wide reserve buffer. |
| 0x38 | 8 | `_IO_buf_end` | End of wide reserve buffer. |
| 0x40 | 8 | `_IO_save_base` | Start of saved wide get area (backup). |
| 0x48 | 8 | `_IO_backup_base` | First valid wide char of backup area. |
| 0x50 | 8 | `_IO_save_end` | End of saved wide get area. |
| 0x58 | 8 | `_IO_state` (`__mbstate_t`) | Current multibyte conversion state. |
| 0x60 | 8 | `_IO_last_state` (`__mbstate_t`) | Previous multibyte conversion state. |
| 0x68 | 0x70 | `_codecvt` (`struct _IO_codecvt`) | Embedded codecvt descriptor. |
| 0xd8 | 4 | `_shortbuf[1]` (`wchar_t`) | Single-wchar fallback buffer. |
| 0xdc | 4 | *(padding)* | Alignment padding before the next 8-byte pointer. |
| 0xe0 | 8 | `_wide_vtable` | Pointer to an `_IO_jump_t` for wide-character operations. |

**Total size: `0xe8` (232 bytes).**

### Notes on the sized fields

- **`__mbstate_t`** is defined in `bits/types/__mbstate_t.h` as a struct containing an `int __count` and a union of an unsigned int and a char array; on 64-bit Linux its size is **8 bytes** (4-byte int + 4-byte value). Two of them occupy 0x58..0x68.
- **`struct _IO_codecvt`** (defined in `libio/libio.h`) is a fixed structure of internal codecvt function pointers and state. On 64-bit glibc 2.42 its size is **0x70 (112 bytes)**, placing it at 0x68..0xd8.
- The trailing alignment after `_shortbuf[1]` is required because the next field, `_wide_vtable`, is an 8-byte pointer and the compiler must align it on an 8-byte boundary.

---

## Summary of total sizes (64-bit, glibc 2.42)

| Struct | Size |
|---|---:|
| `_IO_jump_t` | 0xa8 (168) |
| `_IO_FILE` (prefix) | 0x90 (144) |
| `_IO_FILE_plus` | 0xe0 (224) |
| `_IO_wide_data` | 0xe8 (232) |
