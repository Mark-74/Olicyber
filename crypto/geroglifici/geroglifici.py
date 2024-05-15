import random
import os
import signal
import string

assert("FLAG" in os.environ)
FLAG = os.environ["FLAG"]
assert(FLAG.startswith("flag{"))
assert(FLAG.endswith("}"))

emojis = '🐶🐱🐭🐹🐰🦊🐻🐼🐯🦁🐮🐷🐽🐸🐒🐔🐧🐤🐣🐥🦆🐦🦅🦉🦇🐺🐗🐴🦄🐝🐛🦋🐌🐞🐜🦟🐢🐍🦎🦖🦕🐙🦑🦐🦞🦀🐡🐠🐟🐬🐳🐋🦈🐊🐅🐆🦓🦍🐘🦛🦏🐪🐫🦒🦘🐃🐂🐎🐖🐏🐑🦙🐐🦚🦜🦢🐇🦝🦡🐁🐀🦔🐉'
alphabet = string.ascii_letters + string.digits + '_{}!'


def to_alpha(text):
    res = ''
    for x in text:
        if x in alphabet:
            res += x
    return res[:100]

class Challenge():
    def __init__(self):
        selected = random.sample(emojis, len(alphabet))
        self.code = {x: selected[i] for i, x in enumerate(alphabet)}

    def encode(self, text):
        text = to_alpha(text)
        return ''.join(self.code[x] for x in text)


def main():
    print("Benvenuto aspirante criptoarcheologo!")
    print("Abbiamo trovato un'iscrizione misteriosa nel nostro ultimo scavo...")
    print("Vuoi provare a decifrarla?")

    chall = Challenge()
    print("L'iscrizione recita", chall.encode(FLAG))

    print('Quale messaggio vuoi tradurre?')
    text = to_alpha(input('> '))
    enc = chall.encode(text)
    print(enc)


def handler(signum, frame):
    print("Tempo scaduto!")
    exit()


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)
    main()
