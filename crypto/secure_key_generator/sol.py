from hashlib import sha256
from datetime import datetime
from Crypto.Util.number import long_to_bytes, bytes_to_long
import random
from pwn import xor

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')

file = open("flag.enc", "rb")
text = file.read()
file.close()

#getting seed and key
x = datetime(2021, 3, 21, 17, 37, 40)
date = int(datetime.timestamp(x))
h = sha256(int_to_bytes(date)).digest()
seed = int_from_bytes(h[32:])
key = h[:32]

random.seed(seed)

for _ in range(32):
    key += bytes([random.randint(0, 255)])
    

with open("flag.pdf", "wb") as binary_file:
    
    binary_file.write(xor(text, key))

