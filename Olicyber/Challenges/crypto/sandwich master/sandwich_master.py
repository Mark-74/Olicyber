#!/usr/bin/env python3

import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

flag = os.getenv('FLAG', 'flag{redacted}')

def menu():
    print('''1) sign
2) verify''')
    return int(input('> '))

def mac(k, m):
    cipher = AES.new(k, AES.MODE_CBC, b'\x00'*16)
    if len(m)%16:
        m = pad(m, 16)
    t = cipher.encrypt(m)[-16:]
    return t

def vrfy(k, m, t):
    return mac(k, m) == t

k = os.urandom(16)

msg = b'Im so good with sandwiches they call me mr Krabs'
print(f'Can you authenticate {msg = }?')

while True:
    choice = menu()
    if choice == 1:
        m = bytes.fromhex(input('gimme m: '))
        if m == msg:
            print('that\'s illegal! :(')
            break
        t = mac(k, m)
        print(f'here\'s your tag {t.hex() = }')
    elif choice == 2:
        t1 = bytes.fromhex(input('gimme your tag: '))
        if vrfy(k, msg, t1):
            print(flag)
            break
        else:
            print('oh no :(')
    else:
        print('bye!')
        break
