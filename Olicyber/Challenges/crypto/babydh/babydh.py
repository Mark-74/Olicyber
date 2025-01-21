from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random

with open("flag.txt") as f:
    flag = f.read().strip().encode('utf-8')

g = random.randint(2, 1<<1024)
print(f"g = {g}")

a = random.randint(2, 1<<1024)
b = random.randint(2, 1<<1024)

assert (g + a) + b == (g + b) + a

print(f"g+a = {g+a}")
print(f"g+b = {g+b}")

shared_key = sha256(str(g + a + b).encode()).digest()[:16]
c = AES.new(shared_key, AES.MODE_ECB)
print(f"Encrypted flag: {c.encrypt(pad(flag,16)).hex()}")
