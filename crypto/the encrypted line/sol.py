from Crypto.Util.number import inverse

def decrypt(line, m):
    m = inverse(m, 256)
    res = []
    for x in line:
        res.append((x-1) * m % 256)
    return bytes(res)

def main():
    line = bytes.fromhex("7f1d26c428628a1dd436311d36b0054536f1a79c62f1f59c7b4a8ffc9ca7f19c31bbf16b1dc062e6b2")
    key = inverse(ord("a"), 256) * (line[2]-1) % 256
    print(key)
    print(decrypt(line, key).decode())
    
    
if __name__ == "__main__":
    main()