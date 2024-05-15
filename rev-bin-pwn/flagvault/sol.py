from pwn import *

r = connect("flagvault.challs.olicyber.it", 34000)

print(r.recvline())
r.sendline(b"49CMO:N?O2CD") #la funzione rand ha un seed fisso
r.interactive()