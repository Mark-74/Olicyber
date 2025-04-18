from Crypto.Util.number import getPrime, inverse, long_to_bytes, bytes_to_long


with open("flag.txt") as f:
    flag = f.read().strip().encode('utf-8')


class RSA:
    def __init__(self, nbits, e=-1):
        p, q = getPrime(nbits//2), getPrime(nbits//2)
        N = p*q
        phi = (p-1)*(q-1)
        d = inverse(e, phi)

        self.N = N
        self.e = e
        self.d = d

    def encrypt(self, data):
        m = bytes_to_long(data)
        c = pow(m, self.e, self.N)
        return long_to_bytes(c)

    def decrypt(self, data):
        c = bytes_to_long(data)
        m = pow(c, self.d, self.N)
        return long_to_bytes(m)


rsa = RSA(2048)
flag_enc = rsa.encrypt(flag)

print(f"N = {rsa.N}")
print(f"flag_enc = {flag_enc.hex()}")
