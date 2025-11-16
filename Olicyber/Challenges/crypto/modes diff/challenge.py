#!/usr/bin/env python3

import os
import random
import signal
from Crypto.Cipher import AES

TIMEOUT = 300

assert("FLAG" in os.environ)
flag = os.environ["FLAG"]
key = os.environ["KEY"]
assert(len(key) == 16)
assert(flag.startswith("flag{"))
assert(flag.endswith("}"))


def encrypt_flag():
    iv = os.urandom(16)

    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(flag.encode())
    ciphertext = iv.hex() + encrypted.hex()

    return ciphertext

def decrypt(ciphertext):
    ciphertext = bytes.fromhex(ciphertext)

    cipher = AES.new(key.encode(), AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return str(e)

    return decrypted.hex()

def handle():
    ct = input('ciphertext: ')
    print(decrypt(ct))


if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    handle()
