A = 0x1AACF60
B = 0x4A
C = 0x4B
D = 0x10001

with open("output.txt", "r") as f:
    output = bytes.fromhex(f.read())

for c in output:
    A = (B + A * C) % D
    print(chr(c^(A%256)), end="")
print()