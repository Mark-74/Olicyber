from pwn import *

r = remote("lucky.challs.olicyber.it", 17000)

r.recvuntil(b"key:")

#value obtained by random.c
r.sendline(b"1804289383")
print(r.recvuntil(b'}').decode())

r.close()