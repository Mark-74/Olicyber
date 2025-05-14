from Crypto.Util.number import getPrime, inverse, long_to_bytes, bytes_to_long
from secret import N, e, flag

m = bytes_to_long(flag)
c = pow(m, e, N)
flag_enc = long_to_bytes(c)

print(f"N = {N}")
print(f"e = {e}")
print(f"flag_enc = {flag_enc.hex()}")
