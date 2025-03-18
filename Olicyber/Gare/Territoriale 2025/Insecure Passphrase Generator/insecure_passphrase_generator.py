import os
import string

flag = os.getenv("FLAG", "flag{this_is_a_fake_flag}")

words = [
    "casa", "albero", "notte", "sole", "montagna", "fiume", "mare", "vento", "nuvola", 
    "pioggia", "strada", "amico", "sorriso", "viaggio", "tempo", "cuore", "stella", 
    "sogno", "giorno", "libro", "porta", "luce", "ombra", "silenzio", "fiore", "luna"
]

passphrase = []

for c in flag:
    if c in string.ascii_lowercase:
        passphrase.append(words[ord(c) - ord('a')])
    else:
        passphrase.append(c)


with open("passphrase.txt", 'w') as wf:
    wf.write('-'.join(passphrase))