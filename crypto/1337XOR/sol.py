from pwn import xor

enc_flag = bytes.fromhex("27893459dc8772d66261ff8633ba1e5097c10fba257293872fd2664690e975d2015fc4fd3c")
key = bytearray(xor(b"flag{", enc_flag[0:5]))
print(len(key))

for i in range(256):
    key.append(i) 
    print(xor(enc_flag, key))
    key.pop(5)