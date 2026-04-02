from pwn import remote, xor
from Crypto.Util.Padding import pad

r = remote("privateiv.challs.olicyber.it", 10021)

r.sendlineafter(b"> ", b"1")
r.sendlineafter(b": ", b"00")
r.recvuntil(b": ")
output = bytes.fromhex(r.recvline().strip().decode())
print(pad(b"\x00", 16).hex(), "->", output.hex())

r.sendlineafter(b"> ", b"1")
r.sendlineafter(b": ", (pad(b"\x00", 16) + output).hex().encode())
r.recvuntil(b": ")
output = bytes.fromhex(r.recvline().strip().decode())
to_decipher = output[16:]
print(to_decipher.hex())

r.sendlineafter(b"> ", b"2")
r.sendlineafter(b": ", to_decipher.hex().encode())
r.recvuntil(b": ")
output = bytes.fromhex(r.recvline().strip().decode())[:16].decode()
print(output)

