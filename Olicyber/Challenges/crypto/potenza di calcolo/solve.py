from Crypto.Cipher import AES

p = 159043501668831001976189741401919059600158436023339250375247150721773143712698491956718970846959154624950002991005143073475212844582380943612898306056733646147380223572684106846684017427300415826606628398091756029258247836173822579694289151452726958472153473864316673552015163436466970719494284188245853583109

# Teorema di Wilson
g = -1 % p # non sarebbe g, è congruo a g mod p
a = 3
b = 8

def getDHkey():
    A = pow(g,a,p)
    B = pow(g,b,p)
    K = pow(B,a,p)

    return K

def fakePadding(k):
    if (len(k) > 16):
        raise ValueError('La tua chiave è più lunga di 16 byte')
    else:
        if len(k) == 16:
            return k
        else:
            missingBytes = 16 - len(k)
            for i in range(missingBytes):
                k = ''.join([k,"0"])
            return k

def decrypt(f, k):
    
    key = fakePadding(str(k))
 
    chiave = bytes(key, "utf-8")
    cipher = AES.new(chiave, AES.MODE_ECB)
    decryptedFlag = cipher.decrypt(f)
    return decryptedFlag

ciphertext = bytes.fromhex("b5609cfbad99f1b20ec3a93b97f379d8426f934ffcb77d83ea9161fefa78d243")

print(decrypt(ciphertext, getDHkey()).decode().strip())
