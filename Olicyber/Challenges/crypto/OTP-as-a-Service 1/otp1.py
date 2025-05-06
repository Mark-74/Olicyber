import random
import os
import time

assert("FLAG" in os.environ)
flag = os.environ["FLAG"]
assert(flag.startswith("flag{"))
assert(flag.endswith("}"))

t = int(time.time())
random.seed(t)


def encrypt(data):
    assert isinstance(data, bytes)

    cipher = []
    for b in data:
        r = random.randint(0, 255)
        c = (b+r) % 256
        cipher.append(c)
    return cipher


def intro():
    print("Benvenuto! Questo è OTP-as-a-Service, il sistema di cifratura più sicuro al mondo, gratuito solo per te!")
    print("(è gratis perché è una versione di prova con poche funzionalità)")
    print()
    print("Mandando 'e' puoi farti cifrare la flag, invece con 'q' puoi chiudere la connessione")


def main():
    intro()

    while True:
        try:
            choice = input()
        except:
            exit()

        if choice == "e":
            flag_enc = encrypt(flag.encode())
            print("-".join(map(str, flag_enc)))
        if choice == "q":
            print("Grazie per aver usato OTP-as-a-Service!")
            print("Speriamo ti sia piaciuto, lascia una recensione a 5 stelle!")
            exit()


if __name__ == "__main__":
    main()
