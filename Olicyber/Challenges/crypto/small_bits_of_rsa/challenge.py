#!/bin/env python3

from Crypto.Util.number import bytes_to_long, isPrime
import random, os
from secret import FLAG

def gen_prime(nbits):
    while True:
        x = random.randint(1, nbits-1)
        y = random.randint(1, nbits-1)
        p = 1 + 2**x + 2**y + 2**nbits
        if isPrime(p):
            return p

def keygen(nbits):
    p = gen_prime(nbits//2)
    q = gen_prime(nbits//2)
    n = p*q
    return n


n = keygen(2048)
e = 65537
msg = bytes_to_long(FLAG)
ct = pow(msg, e, n)
print(f"n = {n}")
print(f"ct = {ct}")