#!/usr/bin/env python3

from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad
import random
import os

flag = os.getenv('FLAG', 'flag{REDACTED}')
key = random.getrandbits(60)

def xor(a, b):
    return bytes([x^y for x,y in zip(a,b)])

def encrypt(message, key):
    ivs = [os.urandom(8) for _ in range(3)]

    key1 = key & 0xfffff
    key2 = (key >> 20) & 0xfffff
    key3 = (key >> 40) & 0xfffff

    c1 = Blowfish.new(int.to_bytes(key1, 4, 'big'), Blowfish.MODE_CFB, ivs[0])
    c2 = Blowfish.new(int.to_bytes(key2, 4, 'big'), Blowfish.MODE_CBC, ivs[1])
    c3 = Blowfish.new(int.to_bytes(key3, 4, 'big'), Blowfish.MODE_OFB, ivs[2])

    stream = bytes(len(message))
    stream = pad(stream, 8)

    enc = c1.encrypt(stream)
    enc = c2.encrypt(enc)
    enc = c3.encrypt(enc)

    return b"".join(ivs).hex() + xor(enc, message).hex()

def decrypt(ciphertext, key):
    assert len(ciphertext) > 24

    key1 = key & 0xfffff
    key2 = (key >> 20) & 0xfffff
    key3 = (key >> 40) & 0xfffff

    c1 = Blowfish.new(int.to_bytes(key1, 4, 'big'), Blowfish.MODE_CFB, ciphertext[:8])
    c2 = Blowfish.new(int.to_bytes(key2, 4, 'big'), Blowfish.MODE_CBC, ciphertext[8:16])
    c3 = Blowfish.new(int.to_bytes(key3, 4, 'big'), Blowfish.MODE_OFB, ciphertext[16:24])

    ciphertext = ciphertext[24:]
    stream = bytes(len(ciphertext))
    stream = pad(stream, 8)

    enc = c1.encrypt(stream)
    enc = c2.encrypt(enc)
    enc = c3.encrypt(enc)

    return xor(enc, ciphertext).hex()

for _ in range(256):
    x = input("> ").strip()
    if x[0] == "E":
        print(encrypt(bytes.fromhex(x[1:]), key))
    elif x[0] == "D":
        print(decrypt(bytes.fromhex(x[1:]), key))
    elif x[0] == "G":
        if x[1:] == hex(key)[2:]:
            print(flag)
        else:
            print("Nope")
            exit()

