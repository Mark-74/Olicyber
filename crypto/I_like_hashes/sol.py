from hashlib import sha256
from Crypto.Util.number import long_to_bytes

f = open("ct.txt", 'r')

hashes = f.readlines()
for i in range(len(hashes)): hashes[i] = hashes[i][:len(hashes[i])-1]

for hashed in hashes:
    for i in range(128):
        if sha256(long_to_bytes(i)).digest().hex() == hashed:
            print(chr(i),end="")
            break