from pwn import *

r = remote('software-19.challs.olicyber.it', 13002)
elf = ELF('./sw-19')

r.recvuntil(b'iniziare ...')
r.send(b's')

for i in range(20):
    r.recvuntil(b'-> ')
    symbol = r.recvuntil(b':')[:-1].decode()

    r.sendline(hex(elf.sym[symbol]))
    print(f'{i+1} : {symbol} -> {hex(elf.sym[symbol])}')

print(r.recvline().decode().strip())