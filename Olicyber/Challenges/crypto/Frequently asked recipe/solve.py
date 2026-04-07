import string

with open("ciphertext.txt", "r") as f:
    ciphertext = f.read()

data = {}

for i in range(30):
    data[i] = {}
    for c in ciphertext[i::30]:
        c = c.lower()
        if c not in string.ascii_lowercase:
            continue
        
        if data[i].get(c):
            data[i][c] += 1
        else:
            data[i][c] = 1

for i in range(30):
    data[i] = {k: v for k, v in sorted(data[i].items(), key=lambda item: item[1])}
    
real_data = ["e", "a", "i", "o", "n", "t", "r", "l", "s", "c", "d", "u", "p", "m", "v", "g", "h", "b", "f", "z", "q"]

key = ""
for i in range(30):
    curr = data[i]
    for c in real_data:
        o = ord(max(curr, key=curr.get)) - ord('a')
        cx = ord(c)-ord('a')
        delta = (o - cx) % 26
        print(o, cx, delta)
        print(delta)
        if delta < 10:
            key += str(delta)
            break

    print(key)

    if len(key) != i+1:
        print('key not found')
        exit(1)

def decrypt(s, key):
	# Setup
	final = ''
    # s = perfect(s)
	key = [ int(x) for x in key ]
	key_length = len(key)
	key_index = -1

	for i in range(len(s)):
		element = s[i]
		result = element
		# Char to code
		if ord(element) >= ord('a') and ord(element) <= ord('z'):
			var = ord(element) - ord('a') + 1
		elif ord(element) >= ord('A') and ord(element) <= ord('Z'):
			var = ord(element) - ord('A') + 101
		else:
			var = -100

		# Encrypt
		key_index += 1
		key_index %= key_length
		if var != 0: var -= key[key_index]
		if var > 100:
			if var < 101: var += 26
		else:
			if var < 1: var += 26
		
		# Code to char
		if var >= 1 and var <= 26:
			result = chr(ord('a') + var -1)
		elif var >= 101 and var <= 126:
			result = chr(ord('A') + var - 101)
		final += result
	return final

print(decrypt(ciphertext, key))

# considerazioni fatte a mano
print(key)
key = key[:6] + str(int(key[6]) - 4) + key[7:]
key = key[:2] + str(int(key[2]) + 4) + key[3:]
key = key[:22] + str(int(key[22]) + 4) + key[23:]
key = key[:23] + str(int(key[23]) + 4) + key[24:]
key = key[:24] + str(int(key[24]) + 4) + key[25:]
key = key[:1] + str(int(key[1]) + 4) + key[2:]
key = key[:15] + str(int(key[15]) + 4) + key[16:]
key = key[:17] + str(int(key[17]) - 4) + key[18:]
key = key[:20] + str(int(key[20]) + 4) + key[21:]
key = key[:21] + str(int(key[21]) + 4) + key[22:]
key = key[:9] + str(int(key[9]) + 4) + key[10:]
key = key[:8] + str(int(key[8]) + 4) + key[9:]
print(key)
print(decrypt(ciphertext, key))
print(decrypt(ciphertext, key).find(""))
