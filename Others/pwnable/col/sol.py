from pwn import *

context.binary = elf = ELF('./col')
context.terminal = ('kgx', '-e')

to_reach = 0x21DD09EC
to_reach -= to_reach % 4

to_send = b''
for i in range(5):
    if i == 4:
        to_send += p32(to_reach//5 + 4)
    else:
        to_send += p32(to_reach//5)

if args.GDB:
    r = gdb.debug(['./col', to_send], f'''
              b check_password
              c
                ''')
else:
    r = process(['./col', to_send])

r.interactive()