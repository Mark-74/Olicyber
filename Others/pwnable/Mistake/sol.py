from pwn import *

context.terminal = ('kgx', '-e')

r = process('./mistake')

r.recvline()
r.sendline(b'\2'*10)
r.sendline(b'\3'*10)
r.interactive()
