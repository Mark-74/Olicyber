import random
import os
from secret import flag


def encrypt(data, m, q=1):
    res = []
    for x in data:
        enc = (m*x+q) & 0xff
        res.append(enc)
    return bytes(res)


def main():
    key = 2*random.randint(0, 1 << 128)+1
    ciphertext = encrypt(flag.encode(), key)
    print(ciphertext.hex())


main()
