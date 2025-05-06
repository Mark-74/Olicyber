from pwn import remote
from time import time
import random

r = remote('otp1.challs.olicyber.it', 12304)
t = int(time())

random.seed(t)

r.sendlineafter(b'connessione\n', b'e')
enc = r.recvline().strip().decode().split('-')
r.close()

for j in range(t-10000, t+10000):
    random.seed(j)
    flag = ''
    
    for i in range(0, len(enc)):
        flag += chr((int(enc[i]) - random.randint(0, 255)) % 256)
        
    if flag.startswith('flag{') and flag.endswith('}'):
        print(flag)
        break