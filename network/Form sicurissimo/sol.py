import string

alphabet = string.ascii_lowercase
ciphertext = 'fmcj{yo_ackyzb_ihruvcvjam}'

for i in range(len(ciphertext)):
    if ciphertext[i] == '{' or ciphertext[i] == '}' or ciphertext[i] == '_':
        print(ciphertext[i], end='')
    else:
        print(alphabet[alphabet.find(ciphertext[i])- i], end='')

