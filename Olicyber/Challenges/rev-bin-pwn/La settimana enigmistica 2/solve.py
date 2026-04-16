from pwn import *

board = bytes.fromhex("F9CA3713977605455E49B9D53204FC13BE41AE91D139593B1E02B7C177AEFA9776F9CDD4120C1FCADE688931B2D59A473FD7B07452D8E5719E8FA661F69477C5FEF174D997B361665C6D885232D736D2BF4CE2F0000000000000000000000000")
ids = [int(i) for i in bytes.fromhex("0102030507080B0C0E10111213151718191D1E222427282A2C2E31343538393A3D3F40424345474A4B4C")]
magic = 0x1337CAFE

for i in range(0, len(board), 4):
    tmp = xor(board[i:i+4], p32(magic))
    board = board[:i] + tmp + board[i+4:]
    magic  = (magic * 0x1337) & 0xffffffff

for i in range(9):
    for j in range(9):
        if i*9 + j in ids:
            print("x", end=" ")
            continue
        
        print(board[i*9 + j], end=" ")
    print()

flag = b"flag{219643941755427166311563837545798968172864}"
log.success(flag)

r = process("./enigmista2")
r.sendlineafter(b"> ", flag)
print(r.recvall(timeout=1).decode())
r.close()
