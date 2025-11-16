from pwn import remote, xor

with open('flag.enc', 'r') as f:
    flag = f.read().strip()
    
iv, encrypted_flag = flag[:32], flag[32:]
blocks = [encrypted_flag[i:i+32] for i in range(0, len(encrypted_flag), 32)]

print(f"IV: {iv}")
print(f"Blocks: {blocks}")

# decrypt second block
r = remote("modes.challs.olicyber.it", 10802)
r.sendlineafter(b'ciphertext: ', blocks[1].encode())
response = r.recvline().decode().strip()
r.close()

# decrypt first block
r = remote("modes.challs.olicyber.it", 10802)
r.sendlineafter(b'ciphertext: ', blocks[0].encode())
response2 = r.recvline().decode().strip()
r.close()

print(xor(bytes.fromhex(response2), bytes.fromhex(iv)).decode() + xor(bytes.fromhex(response), bytes.fromhex(blocks[0])).decode())

