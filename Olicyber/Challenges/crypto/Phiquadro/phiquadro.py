from Crypto.Util.number import *
import os

assert("FLAG" in os.environ)
FLAG = os.environ["FLAG"]
assert(FLAG.startswith("flag{"))
assert(FLAG.endswith("}"))

nbits = 2048
p, q = getStrongPrime(nbits), getStrongPrime(nbits)
n = p*q
print(f'{n = }')

phi = (p-1)*(q-1)
leak = pow(phi, 2, n)
print(f'{leak = }')

e = 0x10001
enc_flag = pow(int.from_bytes(FLAG.encode(), 'big'), e, n)
print(f'{enc_flag = }')