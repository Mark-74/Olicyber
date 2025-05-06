from pwn import remote
from tqdm import trange

r = remote('otp2.challs.olicyber.it', 12306)

r.recvuntil(b'connessione\n')

encs = []

for i in trange(5000):
    try:
        r.sendline(b'e')
        encs.append(r.recvline().strip().decode().split('-'))
    except:
        encs.pop()
        r.close()
        r = remote('otp2.challs.olicyber.it', 12306)
        r.recvuntil(b'connessione\n')
        r.sendline(b'e')
        encs.append(r.recvline().strip().decode().split('-'))

r.close()

minimums = [500 for i in range(len(encs[0]))]

for i in range(len(encs)):
    for j in range(len(encs[i])):
        if int(encs[i][j]) < minimums[j]:
            minimums[j] = int(encs[i][j]) # take minimum of each column

        
for c in minimums:
    print(chr(c), end='')
    