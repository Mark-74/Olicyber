#meet in the middle
from hashlib import sha256
from Crypto.Cipher import AES
from pwn import *

def main():
    PASSPHRASE = b"donttrustgabibbo"
    ENCRYPT = ""
    middle = dict()
    
    for i in range(10**6):
        c1 = AES.new(sha256(get_key(str(i)).encode()).digest()[:16], AES.MODE_ECB)
        middle[c1.encrypt(PASSPHRASE)] = i

    r = remote("2fa.challs.olicyber.it", 12206)
    r.recvuntil(b"Esci\n")
    
    r.sendline(b"3")
    r.recvuntil(b":")
    r.recvuntil(b"admin:")
    ENCRYPT = bytes.fromhex(r.recvline().decode()[:-1])
        
    for i in range(10**6):
        c2 = AES.new(sha256(get_key(str(i)).encode()).digest()[:16], AES.MODE_ECB)
        if middle.get(c2.decrypt(ENCRYPT)) is not None:
            print("server key: ", middle[c2.decrypt(ENCRYPT)], "\nuser key: ", i)
            r.interactive()
            break

def get_key(num: str) -> str:
    for i in range(len(num)-6):
        num = "0" + num
    return num

if __name__ == "__main__": 
    main()
