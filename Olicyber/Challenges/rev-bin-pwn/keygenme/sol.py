from pwn import *

context.terminal = ("kgx", "-e")

if args.REMOTE:
    r = remote("keygenme.challs.olicyber.it", 10017)
else:
    r = gdb.debug("./keygenme", '''
                  b *main+80
                  continue
                  ''')
    
r.recvuntil(b"User id: ")

user_id = r.recvline().strip().decode()

p = process(["./sol", user_id])
key = p.recvline().strip()
p.close()

r.sendline(key)
r.interactive()