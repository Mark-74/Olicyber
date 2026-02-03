import os
import signal
from Crypto.Util.number import bytes_to_long

assert ("FLAG" in os.environ)
FLAG = os.environ["FLAG"]
assert (FLAG.startswith("flag{"))
assert (FLAG.endswith("}"))

p = 290413720651760886054651502832804977189
admin_public_key = 285134739578759981423872071328979454683


def menu():
    choice = int(input("""
1) Ottieni la flag
2) Esci
> """))
    if choice not in [1, 2]:
        return None
    return choice


def check_signature(signature, command, pub_key):
    int_command = bytes_to_long(command.encode())

    return (pub_key * signature) % p == int_command


def main():
    print("Benvenuto nel magico sevizio \"Ottieni la flag\". Scegli una delle tante opzioni!")
    while True:
        choice = menu()
        if not choice:
            continue
        if choice == 2:
            print("Addio :(")
            exit()
        else:
            signature = int(input(
                "Dimostrami di essere l'admin, mandami la firma del comando \"get_flag\": "))
            if check_signature(signature, "get_flag", admin_public_key):
                print("Sei sicuramente l'admin, ecco la flag!")
                print(FLAG)
                exit()
            else:
                print("Firma non valida!")
                continue


def handler(signum, frame):
    print("Tempo scaduto!")
    exit()


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)
    main()
