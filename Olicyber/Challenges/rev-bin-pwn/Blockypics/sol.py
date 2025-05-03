from ctypes import CDLL
from pwn import remote
from Crypto.Cipher import AES

libc = CDLL("libc.so.6")
libc.srand(0xE621)
v0 = libc.rand()
libc.srand(v0 % 10000)
v1 = libc.rand()
libc.srand(v1)
v2 = libc.rand()
libc.srand(v2)
v3 = libc.rand()
libc.srand(v3)

def gen1(v, length):
    v2 = libc.rand() & 0xffffffff
    v4 = v2 % length
    result = v2 / length
    
    for j in range(length):
        v7 = v4 + j
        v8 = v[v7 % length]
        
        result = libc.rand() & 0xffffffff
        v[j] = (result ^ v8) & 0xff

def gen2(v, length):
    i = 0
    for i in range(length):
        v3 =  v[libc.rand() % length]
        v[i] = (libc.rand() ^ v3) & 0xff
        
def gen(v, length):
    if libc.rand() & 1:
        gen1(v, length)
    else:
        gen2(v, length)


IV = [0 for _ in range(16)]
KEY = [0 for _ in range(32)]

r = remote("blockypics.challs.olicyber.it", 10805)

encrypted_blocks = []

r.recvline()
for i in range(5):
    print(r.recvline())
    encrypted_blocks.append(bytes.fromhex(r.recvline().strip().decode())) # get the encrypted blocks

r.close()

decrypted_image = b""

for i in range(5):
    gen(KEY, 32)
    gen(IV, 16)
    
    aes = AES.new(bytes(KEY), AES.MODE_CBC, bytes(IV))
    decrypted_image += aes.decrypt(encrypted_blocks[i]) # decrypt the block

with open("decrypted_image.png", "wb") as f:
    f.write(decrypted_image)
    
