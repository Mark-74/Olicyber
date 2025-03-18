from itertools import product
from pwn import xor

# Given SBOX
SBOX = [23, 46, 93, 178, 209, 80, 169, 227, 246, 14, 79, 139, 196, 109, 176, 76, 188, 74, 163, 187, 130, 110, 101, 241, 202, 239, 53, 117, 114, 72, 131, 217, 71, 55, 253, 45, 212, 191, 59, 30, 104, 190, 251, 20, 94, 211, 84, 85, 68, 73, 237, 205, 174, 97, 197, 199, 36, 180, 100, 215, 107, 62, 89, 81, 111, 119, 32, 156, 214, 88, 183, 238, 18, 125, 231, 92, 127, 219, 138, 193, 141, 103, 37, 236, 157, 41, 158, 135, 120, 9, 250, 172, 106, 136, 2, 123, 247, 248, 26, 52, 54, 57, 204, 232, 7, 15, 140, 66, 245, 170, 144, 22, 203, 1, 56, 167, 34, 244, 137, 19, 225, 143, 6, 184, 10, 60, 151, 165, 91, 40, 133, 70, 128, 121, 220, 16, 152, 13, 58, 185, 254, 154, 198, 113, 160, 132, 206, 50, 122, 116, 192, 179, 153, 47, 95, 200, 112, 145, 5, 126, 105, 243, 164, 181, 146, 161, 129, 3, 48, 182, 189, 33, 148, 162, 69, 43, 234, 35, 39, 63, 150, 142, 61, 90, 64, 78, 42, 83, 21, 155, 168, 229, 96, 173, 208, 207, 221, 82, 242, 240, 27, 4, 186, 115, 17, 51, 159, 175, 75, 201, 44, 29, 218, 216, 108, 8, 99, 28, 102, 118, 24, 230, 195, 86, 226, 166, 11, 0, 171, 65, 228, 38, 223, 31, 67, 77, 49, 194, 124, 249, 222, 177, 252, 98, 235, 12, 210, 134, 233, 87, 255, 147, 149, 213, 25, 224]

# Create inverse SBOX
inverse_SBOX = [0] * 256
for i in range(256):
    inverse_SBOX[SBOX[i]] = i

# Read the ciphertext from the file
with open('again_output.txt', 'r') as f:
    hex_str = f.read().strip()
ciphertext = bytes.fromhex(hex_str)

def is_printable(b):
    return 32 <= b <= 126 or b in (9, 10, 13)

# Try possible key lengths
for key_length in range(6, 13):
    # Split into streams
    streams = [[] for _ in range(key_length)]
    for i, byte in enumerate(ciphertext):
        streams[i % key_length].append(byte)
    
    possible_key_bytes = []
    for stream in streams:
        candidates = []
        for key_byte in range(256):
            substituted = [b ^ key_byte for b in stream]
            original = [inverse_SBOX[s] for s in substituted]
            if all(is_printable(b) for b in original):
                candidates.append(key_byte)
        if not candidates:
            break
        possible_key_bytes.append(candidates)
    else:
        # Generate all possible keys
        for key in product(*possible_key_bytes):
            key_bytes = bytes(key)
            # Decrypt
            substituted = xor(ciphertext, key_bytes)
            try:
                plaintext = bytes([inverse_SBOX[b] for b in substituted])
                plaintext_str = plaintext.decode('utf-8')
            except UnicodeDecodeError:
                continue
            # Check for pipe and flag
            if '|' in plaintext_str:
                parts = plaintext_str.split('|')
                if len(parts) >= 2:
                    flag_candidate = parts[-1]
                    if all(c.isalnum() or c in '_{}' for c in flag_candidate):
                        print(f"Key length: {key_length}, Key: {key_bytes.hex()}")
                        print(f"Flag: {flag_candidate}")
                        exit()

print("Flag not found.")
