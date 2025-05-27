#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw
import numpy as np
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

flag = os.getenv('FLAG', 'flag{REDACTED}').encode()

def mix(col1, col2):
    return [(c1 + c2) % 256 for c1, c2 in zip(col1, col2)]

g, a, b = [list(os.urandom(4)) for _ in range(3)]

with Image.open('key_default.png').convert('RGBA') as im:
    n = np.array(im)

n[(n[:, :, 0:4] != [0, 0, 0, 255]).any(2)] = [255,255,255,255]
n[(n[:, :, 0:4] != [255, 255, 255, 255]).any(2)] = g
Image.fromarray(n).save('g.png')
n[(n[:, :, 0:4] != [255, 255, 255, 255]).any(2)] = (A := mix(g, a))
Image.fromarray(n).save('A.png')
n[(n[:, :, 0:4] != [255, 255, 255, 255]).any(2)] = (B := mix(g, b))
Image.fromarray(n).save('B.png')

assert (shared_A := mix(B, a)) == (shared_B := mix(A, b))

cipher = AES.new(sha256(bytes(shared_A)).digest(), AES.MODE_CBC, os.urandom(16))
print((cipher.iv + cipher.encrypt(pad(flag, 16))).hex())
