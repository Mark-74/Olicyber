import random

def encrypt_flag(flag):
    ciphertext = []
    key = random.randint(0, 255)
    random.seed(key)

    for c in flag:
        encrypted_char = c ^ random.randint(0, 255)
        ciphertext.append(encrypted_char)

    return bytes(ciphertext).hex()

flag = open("../flags.txt", "r").read().encode()

encrypted_flag = encrypt_flag(flag)

print(encrypted_flag)