#!/usr/bin/env python3

import os
import signal
from Crypto.Util.number import bytes_to_long, long_to_bytes, getStrongPrime
from random import randint, getrandbits
from Crypto.Cipher import AES

TIMEOUT = 300

assert("FLAG" in os.environ)
flag = os.environ["FLAG"]
assert(flag.startswith("flag{"))
assert(flag.endswith("}"))
assert len(flag) == 25

def generateRSAkey():
    p, q = getStrongPrime(1024), getStrongPrime(1024)
    e = randint(2, (p-1)*(q-1))
    return p*q, e

def handle():
    print('Non ho mai capito quale sia la differenza, in pratica...\n')
    print('1. Invio di un bit della flag')
    print('2. Esci\n')
    n, e = generateRSAkey()
    bitflag = '{:b}'.format(bytes_to_long(flag.encode())).zfill(len(flag)*8)
    b = AES.block_size

    while True:
        scelta = input('> ')
        if scelta == '1':
            msg = getrandbits(2048)
            IV, aes_key = getrandbits(8*b).to_bytes(b, 'big'), getrandbits(8*b).to_bytes(b, 'big')

            try:
                idx = int(input('Quale bit vuoi ricevere? '))

                if int(bitflag[idx]):
                    print(hex(pow(msg,e,n))[2:])
                else:
                    print(AES.new(aes_key, AES.MODE_CBC, IV).encrypt(msg.to_bytes(2048//8, 'big')).hex())

            except Exception as e:
                print(':(')
                return
        else:
            return

    print('Arrivederci!')


if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    handle()
