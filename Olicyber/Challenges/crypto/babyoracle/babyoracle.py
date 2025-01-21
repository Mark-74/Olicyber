from Crypto.Util.number import getPrime, bytes_to_long
import random
import os

assert("FLAG" in os.environ)
flag = os.environ["FLAG"]
assert(flag.startswith("flag{"))
assert(flag.endswith("}"))

NBITS = 1024

p, q = getPrime(NBITS), getPrime(NBITS)
e = 65537
dp = pow(e, -1, (p-1))
enc = pow(bytes_to_long(flag.encode()), e, p*q)

print(f"n = {p*q}")
print(f"encrypted flag = {enc}")

for _ in range(NBITS):
    try:
        ct = int(input("Give me something to decrypt: "))
        assert ct > 0
        assert ct < p*q-1
        assert ct != enc
        print(pow(ct, dp, p))
    except:
        print("Your input is not valid!")
