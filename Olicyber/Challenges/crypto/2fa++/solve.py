from pwn import remote, process, args, log
from tqdm import trange
from hashlib import sha256
from Crypto.Cipher import AES

if args.REMOTE:
    r = remote("2fapp.challs.olicyber.it", 12207)
else:
    r = process("./server.py")

def expand_pin(pin):
    return sha256(pin).digest()[:16]

def hash_psw(pin1, pin2, passphrase):
    c1 = AES.new(expand_pin(pin1), AES.MODE_ECB)
    c2 = AES.new(expand_pin(pin2), AES.MODE_ECB)
    return c1.encrypt(c2.decrypt(c1.encrypt(passphrase))).hex()

def enc(pin, m):
    c1 = AES.new(expand_pin(pin), AES.MODE_ECB)
    return c1.encrypt(m)

def dec(pin, c):
    c1 = AES.new(expand_pin(pin), AES.MODE_ECB)
    return c1.decrypt(c)

map_after_d2    = dict()

SENDING_SIZE = 10000
for i in trange(0, 10**6, SENDING_SIZE):
    r.sendlineafter(b'Esci\n\n', b'3')
    r.sendlineafter(b'Username: ', b'admin')
    r.sendlineafter(b'Password per il recupero (hex): ', ''.join([dec(pin, b"gabibbo_hates_me").hex() for pin in [str(i + j).zfill(6).encode() for j in range(SENDING_SIZE)]]).encode())
    r.recvuntil(b'DEBUG token calcolato: ')
    token = bytes.fromhex(r.recvline().strip().decode())
    for j in range(SENDING_SIZE):
        map_after_d2[dec(str(i + j).zfill(6).encode(), token[j*16:(j+1)*16])] = str(i + j).zfill(6)

pins = ('', '')

for i in trange(10**6):
    pin2 = str(i).zfill(6).encode()
    enc = dec(pin2, b"gabibbo_hates_me")
    if map_after_d2.get(enc) is not None:
        pins = (map_after_d2[enc], str(i).zfill(6))
        log.success(f"Pin 1: {pins[0]}, Pin 2: {pins[1]}")
        break

if pins == ('', ''):
    log.failure("No pin :(")
    exit(1)

r.sendlineafter(b'Esci\n\n', b'2')
r.sendlineafter(b'Username: ', b'admin')
r.sendlineafter(b'Pin personale: ', pins[0].encode())
r.sendlineafter(b'Pin del server: ', pins[1].encode())

print(r.recvall(timeout=2).decode())