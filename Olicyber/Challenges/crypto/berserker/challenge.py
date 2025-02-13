#!/usr/bin/env python3

import os
import signal
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

TIMEOUT = 300

flag = 'flag{' + 'a'*26 + '}'
assert len(flag) == 32

def xor(a,b):
    return bytes([x^y for x,y in zip(a,b)])

def handle():
    b = AES.block_size
    print(b)
    aes_key = os.urandom(b)
    print('1. Registrazione')
    print('2. Cifra un messaggio')
    print('3. Esci dal programma')
    while True:
        cookie_di_sessione = None
        scelta = input('> ')

        if scelta == '1':
            name = input('Come ti chiami? ')
            cookie = pad(f'user={name};flag={flag}'.encode(), b)
            ciphertext = b''    
            IV = os.urandom(b)
            for block in [cookie[i:i+b] for i in range(0, len(cookie), b)]:
                print('blocco ', block)
                ciphertext += AES.new(aes_key, AES.MODE_ECB).encrypt(xor(block,IV))
                IV = ciphertext[-b:]
            cookie_di_sessione = ciphertext
            print('Cookie di sessione cifrato:', ciphertext.hex())

        elif scelta == '2':
            if not cookie_di_sessione:
                print('E\' necessaria la registrazione prima di procedere con la cifratura dei messaggi.')
            try:
                msg = pad(bytes.fromhex(input('Inserisci il messaggio da cifrare (hex): ')), b)
            except Exception:
                print('Qualcosa è andato storto con il tuo input...')
                return
            ciphertext = b''
            for block in [msg[i:i+b] for i in range(0, len(msg), b)]:
                print('blocco ', block)
                ciphertext += AES.new(aes_key, AES.MODE_ECB).encrypt(xor(block,IV))
                IV = ciphertext[-b:]
            print('Messaggio cifrato:', ciphertext.hex())

        else:
            print('Arrivederci!')
            return



if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    handle()
