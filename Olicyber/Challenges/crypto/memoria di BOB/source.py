#!/usr/bin/python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode
from signal import alarm as timeout

key = b""
chat = b"????"
cipher = AES.new(key, AES.MODE_ECB)


def main():
    mittente = b"Bob: "
    loop = '1'
    while loop == '1':
        msg = input(f'Dammi il tuo messaggio segreto:\n{mittente}').encode()
        plaintext = mittente + msg + chat
        ciphertext = cipher.encrypt(pad(plaintext, 16))
        print('ecco la nostra conversazione super protetta. Nessuno potrà decriptare questo messaggio!')
        print(b64encode(ciphertext).decode())
        loop = input(
            'non è il messaggio che volevi mandare?\nRiprova pure premendo 1\n')[0]
    print('ciao ;-)')


if __name__ == '__main__':
    timeout(300)
    main()
