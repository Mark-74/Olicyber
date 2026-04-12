from pwn import remote, xor
import base64

r = remote("flip.challs.olicyber.it", 10603)

command = b"Dammi la flaaag!"
r.sendlineafter(b"!!!", b"1")
r.sendlineafter(b"Messaggio: ", command)

ciphertext = r.recvline().decode().strip().split(": ")[1]
IV = r.recvline().decode().strip().split(": ")[1]

print(ciphertext, IV)

IV = base64.b64decode(IV)
IV = xor(IV, b"\x00"*10 + b"false,")
IV = xor(IV, b"\x00"*10 + b"true, ")
IV = base64.b64encode(IV)

r.sendlineafter(b"!!!", b"2")
r.sendlineafter(b"ordine: ", ciphertext.encode())
r.sendlineafter(b"IV: ", IV)

r.recvuntil(b"Ciao capo!\n")
print(r.recvline().strip().decode())

r.close()
