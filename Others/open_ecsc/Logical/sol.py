from Crypto.Util.number import long_to_bytes
from pwn import remote

r = remote('logical.challs.cyberchallenge.it', 38207)

r.recvuntil(b'> ')
r.sendline(b'2')

enc_flag = int(r.recvline())
n = int(enc_flag.bit_length()/2+0.5)

r.sendline(b'1')
r.recvuntil(b'> ')
r.sendline(b'\0') #sending a 0 byte, so res never gets xored with 1
r.recvuntil(b'> ')
r.sendline(b'2')
r.recvline()

enc_note = int(r.recvline())

r.close()

secret_key = enc_note
flag = ''

for i in range(n):
    if (secret_key & 1) != (enc_flag & 1):
        flag = '1' + flag
    else:
        flag = '0' + flag
    secret_key >>= 2
    enc_flag >>=2

print(long_to_bytes(int(flag, 2)))