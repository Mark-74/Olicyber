key =    bytearray(bytes.fromhex("532B412E9287C0F0358B9CC383866FF8"))
target = bytearray(bytes.fromhex("272D20263A3629702D72701E3971333C"))

def rotate_key():
    global key
    key = key[1:] + key[0].to_bytes(1, 'big')

for i in range(16):
    rotate_key()
    for j in range(16):
        target[j] ^= key[j]
        

print(target.decode())