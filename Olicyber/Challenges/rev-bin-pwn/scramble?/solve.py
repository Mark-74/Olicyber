from pwn import args, remote, process
import string

if args.REMOTE:
    r = remote("scramble.challs.olicyber.it", 11304)
    delimiter = b"\r\n"
else:
    r = process("./chall.py")
    delimiter = b"\n"


# recover shift
alph = string.ascii_uppercase+string.ascii_lowercase # il sort così non cambia questa stringa
r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"string?"+delimiter, alph.encode())
res = r.recvline().strip().decode()
shift = len(res) - res.index('A')
print(f"Shift for this connection: {shift}")

# recover charsf, cashrsn and chars for flag
r.sendlineafter(b"> ", b"2")
enc = r.recvline().strip().decode()
# enc contiene le stesse lettere di flag ma solo shiftate
charsf = {}
for c in enc:
    if c not in charsf.keys():
        charsf[c] = 1
    else:
        charsf[c] += 1
print("charsf map:\t", charsf)
chars = list(charsf.keys())
chars.sort(reverse=True, key=lambda e: charsf[e])
print("sorted chars:\t", chars)
charsn = list(chars)
for _ in range(shift):
    i = charsn.pop(0)
    charsn.append(i)

# recover flag
for c in enc:
    print(chars[charsn.index(c)], end="")
print()
