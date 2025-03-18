
words = [
    "casa", "albero", "notte", "sole", "montagna", "fiume", "mare", "vento", "nuvola", 
    "pioggia", "strada", "amico", "sorriso", "viaggio", "tempo", "cuore", "stella", 
    "sogno", "giorno", "libro", "porta", "luce", "ombra", "silenzio", "fiore", "luna"
]

with open("passphrase.txt", "r") as f:
    passphrase = f.read().strip()

flag = []
for part in passphrase.split("-"):
    if part in words:
        # Convert word to corresponding lowercase letter
        letter = chr(words.index(part) + ord('a'))
        flag.append(letter)
    else:
        # Add non-lowercase characters (e.g., '{', '}') directly
        flag.append(part)

print("".join(flag))
