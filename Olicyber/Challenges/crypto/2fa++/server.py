#!/usr/bin/env -S python3
from Crypto.Cipher import AES
from Crypto.Random.random import randint
from hashlib import sha256
import signal
import os
import sys
flag = os.environ.get("FLAG", "flag{fake_flag_for_testing}")
assert(flag.startswith("flag{"))
assert(flag.endswith("}"))

allow_pin_recover = False # Funzione ancora in beta, meglio disabilitarla per ora
allow_user_list = False # Meglio disabilitare anche questo, c'è qualcosa che non mi convince nella versione precedente...

db = {}
recover_db = {}

def handler(signum, frame):
    print("Tempo scaduto!")
    exit()

def hash_psw(pin1, pin2, passphrase = b"donttrustgabibbo"):
    c1 = AES.new(expand_pin(pin1), AES.MODE_ECB)
    c2 = AES.new(expand_pin(pin2), AES.MODE_ECB)
    return c1.encrypt(c2.decrypt(c1.encrypt(passphrase))).hex()

def login():
    username = input("Username: ").encode()
    user_pin = input("Pin personale: ").encode()
    server_pin = input("Pin del server: ").encode()

    if username not in db:
        print("Username non trovato")
    elif db[username] != hash_psw(user_pin, server_pin):
        print(f"Autenticazione fallita.")
    else:
        print(f"Login effettuato come {username.decode()}")
        if username == b"admin":
            print(flag)

def register():
    username = input("Scegli uno username di almeno 3 caratteri: ")
    if username.encode() in db or len(username) < 3:
        print("Username già utilizzato o troppo corto!")
        return
    user_pin = input("Scegli un pin personale di 6 cifre: ").encode()
    if not user_pin.isdigit() or len(user_pin) != 6:
        print("Pin non valido")
        return
    passphrase = input("Password per il recupero del pin (in hex, 16 bytes): ")
    if len(passphrase) != 32:
        print("La password non ha la lunghezza giusta!")
        return
    try:
        passphrase = bytes.fromhex(passphrase)
        server_pin = str(randint(1,999999)).zfill(6)
        print(f"Pin del server per l'utente {username}: {server_pin}")
        token = hash_psw(user_pin, server_pin.encode())
        token2 = hash_psw(user_pin, server_pin.encode(), passphrase)
        db[username.encode()] = token
        recover_db[username.encode()] = (user_pin, server_pin.encode(), token2)
        print(f"Utente {username}:{token} creato con successo!")
    except:
        print("Qualcosa è andato storto...")

def pin_recover():
    username = input("Username: ").encode()
    passphrase = input("Password per il recupero (hex): ")
    passphrase = bytes.fromhex(passphrase)
    if username not in db:
        print("Username non trovato")
    else:
        pin1, pin2, token = recover_db[username]
        pass_token = hash_psw(pin1, pin2, passphrase)
        print(f"DEBUG token calcolato: {pass_token}") # TODO: rimuovere
        if pass_token == token and allow_pin_recover:
            print(pin1, pin2)
        else:
            print("Pin non valido o funzione disabilitata dall'amministratore.")

def users_list():
    if allow_user_list:
        print("Utenti attualmente registrati:")
        for u in db:
            print(f"\t{u.decode()}:{db[u]}")
    else:
        print("Funzione disabilitata!")

def initialize_db():
    admin_pin1 = str(randint(1,999999)).zfill(6).encode()
    admin_pin2 = str(randint(1,999999)).zfill(6).encode()
    admin_token = hash_psw(admin_pin1, admin_pin2)
    db[b"admin"] = admin_token
    rec_token = hash_psw(admin_pin1, admin_pin2, b"gabibbo_hates_me")
    recover_db[b"admin"] = (admin_pin1, admin_pin2, rec_token)

def expand_pin(pin):
    return sha256(pin).digest()[:16]

def menu():
    print()
    print("Cosa vuoi fare?")
    print("1. Registrazione")
    print("2. Login")
    print("3. Recupero pin")
    print("4. Lista utenti")
    print("0. Esci")
    print()

    try:
        choice = int(input())
        assert choice in [0,1,2,3,4]
        if choice == 1:
            register()
        elif choice == 2:
            login()
        elif choice == 3:
            pin_recover()
        elif choice == 4:
            users_list()
        else:
            exit()
    except Exception as e:
        print("Opzione non valida!")

initialize_db()
signal.signal(signal.SIGALRM, handler)
signal.alarm(180)
while True:
    menu()
