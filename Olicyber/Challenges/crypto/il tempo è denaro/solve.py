from pwn import remote
from tqdm import trange

r = remote("time.challs.olicyber.it", 10505)

flag = ""
for i in trange(25*8):
    different_len = False
    for j in range(50):
        try:
            r.sendlineafter(b"> ", b"1")
            r.sendlineafter(b"? ", str(i).encode())
            enc = r.recvline().strip().decode()
            if len(enc) != 512:
                different_len = True
                break
        except:
            j -= 1
            r.close()
            r = remote("time.challs.olicyber.it", 10505)

    if different_len:
        flag += "1"
    else:
        flag += "0"

print(flag)
s = int(flag, 2).to_bytes(len(flag) // 8, 'big').decode()
print(s)
