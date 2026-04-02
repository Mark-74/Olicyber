#!/usr/bin/env python3

import os
import signal
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

TIMEOUT = 300

assert("FLAG" in os.environ)
flag = os.environ["FLAG"]
assert(flag.startswith("flag{"))
assert(flag.endswith("}"))


def encrypt(message): #message is in hexadecimal form
    cipher = AES.new(flag.encode(),AES.MODE_CBC,flag.encode())
    ciphertext = cipher.encrypt(pad(bytes.fromhex(message),16))
    return ciphertext.hex()

def decrypt(ciphertext): #ciphertext is in hexadecimal form
    cipher = AES.new(flag.encode(),AES.MODE_CBC,flag.encode())
    plaintext = cipher.decrypt(bytes.fromhex(ciphertext))
    return plaintext.hex()


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def handle():
    print('Benvenuto!')
    print('Cosa vuoi fare?')

    while(True):
        print('1. Encrypt')
        print('2. Decrypt')
        res = int(input('\n> '))

        if res == 1:
            message = input('\nInserisci il messaggio: ')
            ciphertext = encrypt(message)
            print("Il messaggio criptato è: {0}".format(ciphertext))
        elif res == 2:
            ciphertext = input('\nInserisci il messaggio: ')
            plaintext = decrypt(ciphertext)
            print("Il messaggio decriptato è: {0}".format(plaintext))
        else:
            return
        


    return


if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    handle()
