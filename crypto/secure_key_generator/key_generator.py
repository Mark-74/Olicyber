#!/usr/bin/env python3

from hashlib import sha256
from datetime import datetime
import random


# 2021-03-21 17:37:40

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')

def generate_secure_key():
    ts = int(datetime.timestamp(datetime.now()))
    h = sha256(int_to_bytes(ts)).digest()

    seed = int_from_bytes(h[32:])
    key = h[:32]
    
    random.seed(seed)
    for _ in range(32):
        key += bytes([random.randint(0, 255)])


    return key
