from math import gcd
from pwn import remote
from Crypto.Util.number import bytes_to_long

p                   = 290413720651760886054651502832804977189
admin_public_key    = 285134739578759981423872071328979454683
d = gcd(admin_public_key, p)

signature = bytes_to_long(b'get_flag') * pow(admin_public_key, -1, p//d) % (p//d)
print(signature)

r = remote("il-solito-servizio.challs.olicyber.it", 34006)
r.sendlineafter(b'opzioni!', b'1')
r.sendlineafter(b'firma del comando "get_flag": ', str(signature).encode())
print(r.recvall(timeout=1).decode())