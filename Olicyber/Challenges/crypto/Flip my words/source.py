from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
from base64 import b64encode, b64decode
import json
from signal import alarm as timeout

FLAG = "???????"
key = os.urandom(16)


def main():
    IV = os.urandom(16)
    loop = True
    while loop:
        choice = input("""
Cosa vuoi fare?
1) Cripta un messagio
2) Decripta un messagio
altro) lascia questo posto!!!
""").strip()
        if choice == '1':
            msg = input('che messaggio vuoi criptare?\nMessaggio: ')
            plaintext = json.dumps({'admin': False, 'msg': msg}).encode()
            # IV non viene risettato per permettere l'inserzione di blocchi
            cipher = AES.new(key, AES.MODE_CBC, IV)
            ciphertext = cipher.encrypt(pad(plaintext, 16))
            print(
                f"Ecco qui la tua richiesta: {b64encode(ciphertext).decode()}\nE questo è l'IV: {b64encode(IV).decode()}")
        elif choice == '2':
            ciphertext = input("Vuoi dire qualcosa?\nInserisci un ordine: ")
            IV = input("Hai un IV?\nIV: ")
            ciphertext, IV = b64decode(ciphertext), b64decode(IV)
            cipher = AES.new(key, AES.MODE_CBC, IV)
            cookie = unpad(cipher.decrypt(ciphertext), 16)
            print(cookie)
            cookie = json.loads(cookie)
            plaintext = cookie["msg"]
            admin = cookie["admin"]
            print(plaintext, cookie)
            if admin:
                print("Ciao capo!")
                if plaintext == "Dammi la flaaag!":
                    print(f"Eccola: {FLAG}")
            else:
                print(f"Caro utente, il comando {msg} non può essere eseguito")
        else:
            loop = False
            print("ciao")


if __name__ == '__main__':
    timeout(300)
    main()
