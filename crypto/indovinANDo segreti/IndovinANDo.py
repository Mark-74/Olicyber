import random
import os
import signal

assert("FLAG" in os.environ)
FLAG = os.environ["FLAG"]
assert(FLAG.startswith("flag{"))
assert(FLAG.endswith("}"))


class Challenge:
    def __init__(self):
        self.s = os.urandom(8)
        self.P = list(range(256))
        random.shuffle(self.P)

    def query(self, i):
        return bytes([x & self.P[i] for x in self.s])

    def guess(self, g):
        return bytes.fromhex(g) == self.s


def main():
    print("Benvenuto a indovina il segreto!")
    print("Se riuscirai a indovinare per 10 volte di fila, ti svelerò una bellissima flag!")

    for i in range(10):
        chall = Challenge()
        print(f"Round {i+1} di 10")
        while True:
            q = input(">")
            if q == "g":
                break
            print(chall.query(int(q)).hex())
        guess = input("Qual è il segreto di questo round?")
        if not chall.guess(guess):
            print("NOPE")
            exit(2)

    print(FLAG)
    return


def handler(signum, frame):
    print("Tempo scaduto!")
    exit()


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)
    main()
