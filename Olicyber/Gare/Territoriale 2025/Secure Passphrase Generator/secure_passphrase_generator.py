#!/usr/bin/env python3

import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import random

users = []
flag = os.getenv('FLAG', 'flag{redacted!!}')
flag_blocks = [flag[i:i+len(flag)//4] for i in range(0, len(flag), len(flag)//4)]
assert len(flag_blocks) == 4
key = os.urandom(16)
words = flag_blocks + [
    "Girasole", "Tempesta", "Mistero", "Orologio", "Sussurro",
    "Fragile", "Caminetto", "Riflesso", "Labirinto", "Cristallo",
    "Nebbia", "Eclissi", "Farfalla", "Crepuscolo", "Onda",
    "Radice", "Specchio", "Melodia", "Ombra", "Incanto"
]

def parse(s):
    res = {}
    for item in s.split(';'):
        key, value = item.split('=')
        res[key] = value
    return res


def generate():
    username = input('Username? ')
    if username in users:
        print("L'utente è già registrato")
        return
    indexes = [random.randint(4, len(words) - 1) for _ in range(4)]
    passphrase = '-'.join(words[i] for i in indexes)
    print(f"La tua passphrase è {passphrase}")

    token = f'username={username};index0={indexes[0]};index1={indexes[1]};index2={indexes[2]};index3={indexes[3]}'
    print(f"Token: {token}")
    iv = os.urandom(16)
    enc = AES.new(key, mode=AES.MODE_CBC, iv=iv).encrypt(pad(token.encode(), 16))
    print(f'Nel caso la dimenticassi, puoi recuperarla con il seguente token: {(iv + enc).hex()}')
    users.append(username)


def recover():
    enc_token = bytes.fromhex(input('Token? '))
    iv, ciphertext = enc_token[:16], enc_token[16:]
    token = parse(unpad(AES.new(key, mode=AES.MODE_CBC, iv=iv).decrypt(ciphertext), 16).decode('utf-8'))
    
    # aggiunto
    print(f"Token decifrato: {token}")

    if token['username'] not in users:
        print("Il token non è valido")
    else:
        indexes = [token['index0'], token['index1'], token['index2'], token['index3']]
        passphrase = '-'.join(words[int(i)] for i in indexes)
        print(f"La tua passphrase è {passphrase}")


if __name__ == "__main__":
    print("Benvenuto! Qui puoi generare le tue passphrase in modo veloce e sicuro! Inoltre hai a disposizione un token per recuperarle ogni volta che le dimentichi")
    menu = "1. Genera passphrase\n2. Recupera passhrase\n3. Esci"
    while True:
        print(menu)
        choice = int(input('> '))
        if choice == 1:
            generate()
        elif choice == 2:
            recover()
        else:
            exit()
