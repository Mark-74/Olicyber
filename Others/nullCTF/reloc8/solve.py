#!/usr/bin/env python3

import base64
from pwn import *

elf = ELF("./d8_patched")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        r = remote("34.118.61.99", 10143)
    elif args.GDB:
        r = gdb.debug([elf.path, "--allow-natives-syntax", "solve.js"], '''
                                continue
                      ''')
    else:
        r = process([elf.path, "--allow-natives-syntax", "solve.js"])

    return r


def main():
    r = conn()

    if args.REMOTE:
        with open("solve.js", "rb") as f:
            code = f.read().replace(b"%", b"//%")  
        enc = base64.b64encode(code)
        r.sendlineafter(b"Code (base64): ", enc)

    r.interactive()


if __name__ == "__main__":
    main()

