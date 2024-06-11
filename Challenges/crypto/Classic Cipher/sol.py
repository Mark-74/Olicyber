alphabet = "abcdefghijklmnopqrstuvwxyz"

def generateKey(start): #start va da 1 a 25
    key = "".join([alphabet[start:], alphabet[0:start]]) #aplhabet[start] + alphabet[da 0 a start -1]
    return key

def decrypt(ciphertext, key):
    plain = ""
    print("key: " + key)
    for i in reversed(range(len(ciphertext))):
        if(ord(ciphertext[i]) <= 122 and ord(ciphertext[i]) >= 97):
            key = "".join([key[1:len(key)], key[0]]) #shifto la key di una pos a sx
            j = key.index(ciphertext[i])
            print(j,end=" ")
            plain = "".join([alphabet[j], plain])
        else:
            plain = "".join([ciphertext[i], plain])

    return plain

for i in range(1,25):
    print(decrypt("xcqv{" + "gvyavn_zvztv_etvtddlnxcgy}", generateKey(i)))
