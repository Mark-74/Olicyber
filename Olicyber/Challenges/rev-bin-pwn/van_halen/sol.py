data = [ 0x66, 0x6d, 0x63, 0x64, 0x7f, 0x62, 0x36, 0x58, 0x3c, 0x61, 0x39, 0x6a, 0x68, 0x52, 0x3a, 0x61, 0x74, 0x4e, 0x78, 0x66, 0x79, 0x65, 0x6b, 0x17 ]

for i in range(24):
    print(chr(data[i] ^ i),end="")