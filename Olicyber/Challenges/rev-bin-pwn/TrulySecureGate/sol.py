from pwn import *

r = remote('tsg.challs.olicyber.it', 14000)

r.recvuntil(b'$ ')
r.sendline(b'cat flag.txt')
r.recvuntil(b'Password: ')
r.sendline(b'hehethistimeyouwontfindthis') #found with gdb: the program calculates the password and then compares it with our input, this is the calculated password
print(r.recvline().decode().strip())

r.close()