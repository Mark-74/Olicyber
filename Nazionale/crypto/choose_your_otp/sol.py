from pwn import remote
from Crypto.Util.number import long_to_bytes

r = remote('192.168.100.3', 38302)

r.sendlineafter('> ', str(2**200))
num = int(r.recvline())
r.close()

for i in range(0, 2**200):
    if b'flag' in long_to_bytes(i ^ num):
        print(long_to_bytes(i ^ num))
        