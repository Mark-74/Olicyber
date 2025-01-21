from pwn import *

alphabet = string.ascii_letters + string.digits + '_{}!'
emojis = '🐶🐱🐭🐹🐰🦊🐻🐼🐯🦁🐮🐷🐽🐸🐒🐔🐧🐤🐣🐥🦆🐦🦅🦉🦇🐺🐗🐴🦄🐝🐛🦋🐌🐞🐜🦟🐢🐍🦎🦖🦕🐙🦑🦐🦞🦀🐡🐠🐟🐬🐳🐋🦈🐊🐅🐆🦓🦍🐘🦛🦏🐪🐫🦒🦘🐃🐂🐎🐖🐏🐑🦙🐐🦚🦜🦢🐇🦝🦡🐁🐀🦔🐉'

r = remote("geroglifici.challs.olicyber.it", 35000)

r.recvuntil(b"recita ")
FLAG = r.recvline().decode()[:-1]
r.recvuntil("> ")

r.sendline(b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}!")
leak = r.recvline().decode()[:-1]

mappa = dict()
for i in range(len(alphabet)):
    mappa[leak[i]] = alphabet[i]

for i in FLAG:    
    print(mappa[i], end="")