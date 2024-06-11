from pwn import remote

r = remote('chooseyourotp.challs.olicyber.it', 38302)

result = ''

for i in range(400):
    print(r.recvuntil('> '), i)
    r.sendline(str(2**i))
    result = str(int(r.recvline()) >> i) + result
    
print(int(result, 2).to_bytes((len(result) + 7) // 8, byteorder='big'))