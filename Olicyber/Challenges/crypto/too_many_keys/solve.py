from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from math import gcd

keys = []
e = 65537

with open("./root.pem", "rb") as f:
    root_key = RSA.import_key(f.read()).n

for i in range(1, 51):
    with open(f"./keys/key_{i}.pem", "rb") as f:
        key = RSA.import_key(f.read())
    keys.append(key.n)

for i in range(50):
    _gcd = gcd(keys[i], root_key)
    if _gcd != 1:
        p, q = _gcd, root_key // _gcd
        phi = (p-1)*(q-1)
        d = pow(e, -1, phi)

        with open("./flag.txt.enc", "rb") as f:
            c = bytes_to_long(f.read())
        m = pow(c, d, root_key)
        print(long_to_bytes(m))

        exit(0)

exit(1)

