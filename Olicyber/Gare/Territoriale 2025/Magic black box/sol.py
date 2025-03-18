from pwn import remote
from ctypes import CDLL

libc = CDLL('libc.so.6')
final = bytearray(bytes.fromhex('1f84e6290b29a50954607fb2ad6615796a522d688d89acffe95a771ce9ba0d12b0288d7c'))
libc.srand(0x1337 & 0xffffffff)
rands = [libc.rand() for _ in range(500)]

def xor(block, rand):
    rand &= 0xff
    for i in range(36):
        block[i] ^= rand
    return block

def add(block, rand):
    rand &= 0xff
    for i in range(36):
        block[i] = (block[i] + rand) & 0xff
    return block

def sub(block, rand):
    rand &= 0xff
    for i in range(36):
        block[i] = (block[i] - rand) & 0xff
    return block

def ror_left(block, rand):
    copy = block.copy()
    for i in range(36):
        block[i] = copy[(i + rand % 36) % 36]
    return block

def ror_right(block, rand):
    copy = block.copy()
    for i in range(36):
        block[i] = copy[(i - rand % 36 + 36) % 36]
    return block

operations          = [xor, add, sub, ror_left, ror_right]
reversed_operations = [xor, sub, add, ror_right, ror_left]

block = final
for i in reversed(range(500)):
    block = reversed_operations[i % 5](block, rands[i])

print(block.hex())

r = remote('magicbb.challs.olicyber.it', 38050)
r.sendafter(b':)\n', block.hex().encode())
print(r.recvall().strip().decode())
r.close()
