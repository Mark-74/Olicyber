import sys
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <file to encrypt>')
    exit(0)

CHUNK_SIZE = 13337

file_to_encrypt = sys.argv[1]
readfile = open(file_to_encrypt, 'rb')
content = readfile.read()
readfile.close()

chunks = [content[CHUNK_SIZE*i:CHUNK_SIZE*(i+1)] for i in range(len(content) // CHUNK_SIZE + 1)]

for i, chunk in enumerate(chunks):
    iv = b'\x00' * 16
    cipher = AES.new(sha256(file_to_encrypt.encode()).digest(), mode=AES.MODE_CBC, iv=iv)
    enc = cipher.encrypt(pad(chunk, AES.block_size))
    writefile = open(f'encrypted_chunks/{file_to_encrypt}_{i:02}.enc', 'wb')
    writefile.write(enc)
    writefile.close()
