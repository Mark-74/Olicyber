from Crypto.Util.number import long_to_bytes

encs = [int(_) for _ in open("encryptions.txt", "r").read().splitlines()]

'''
A, B = encs[0], encs[1]

(x + 2y) % k = A % k
(x + 3y) % k = B % k

y % k = (B - A) % k
x % k = (A - 2y) % k
'''

# si poteva pure brutare
K = 2 ** max([enc.bit_length() for enc in encs])

print("K =", K)
for enc in encs:
    if enc != enc % K:
        print("Error: invalid K")
        exit(1)

A, B = encs[0], encs[1]

KEY = (B - A) % K
FLAG = (A - 2 * KEY) % K

print("FLAG =", long_to_bytes(FLAG).decode())