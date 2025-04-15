from pwn import remote
from Crypto.Util.number import long_to_bytes
def xor(a: str, b: str) -> str:
    if a != b:
        return '1'
    else:
        return '0'

output = 0xe05b

def checksum(input: bytes):
    res = 0xffff
    
    for i in range(len(input)):
        ch = (input[i] & 0xff) ^ ((res >> 8) & 0xff)
        ch = ch ^ (ch >> 4)
        res = (0xffff & ch) ^ (0xffff & (res << 8)) ^ (0xffff & (ch << 0xc)) ^ (0xffff & (ch << 5))
    
    return res
    

_input = b''
    
for i in range(2**(30*8)):
    _input = long_to_bytes(i)
    if checksum(_input) == output:
        print(f"Found: {_input}")
        break
    
r = remote('crc.challs.olicyber.it', 12201)
r.sendlineafter(b'password:', _input)
print(r.recvline().strip().decode())
