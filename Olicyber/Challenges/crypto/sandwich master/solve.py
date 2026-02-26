from pwn import args, remote, process, xor
from Crypto.Util.Padding import pad

if args.REMOTE:
    r = remote("sandwichmaster.challs.olicyber.it", 30996)
else:
    r = process("./sandwich_master.py")
    
msg = b'Im so good with sandwiches they call me mr Krabs'

print(r.sendlineafter(b'>', b'1'))
r.sendlineafter(b'm:', pad(b'a', 16).hex().encode())
r.recvuntil(b'= \'')
c1 = bytes.fromhex(r.recvuntil(b'\'\n', drop=True).decode()) # output of mac(k, pad(b'a', 16))

blocks = [pad(b'a', 16).hex().encode()] + [msg[i:i+16].hex().encode() for i in range(0, len(msg), 16)]
blocks[1] = xor(c1, bytes.fromhex(blocks[1].decode())).hex().encode() # by xoring the first block's output with the second block, the status is restored and thus c1 = mac(k, pad(b'a', 16)) -> mac(k, msg) = mac(k, pad(b'a', 16) + msg[:16] ^ c1 + msg[16:])

for i in blocks:
    print(len(i), i)

r.sendlineafter(b'>', b'1')
r.sendlineafter(b'm:', b''.join(blocks))

r.recvuntil(b'= \'')
tag = bytes.fromhex(r.recvuntil(b'\'\n', drop=True).decode())
r.sendlineafter(b'>', b'2')
r.sendlineafter(b'tag:', tag.hex().encode())

print(r.recvall(timeout=2).decode())
