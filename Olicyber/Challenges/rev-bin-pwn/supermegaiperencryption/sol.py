from pwn import *

if args.REMOTE:
    r = remote("supermegaiperencryption.challs.olicyber.it", 10803)
else:
    r = process("./supermegaiperencryption")

r.recvuntil(b"supercriptazione:\n")
output = r.recvline().decode().strip()

print("level 3 output:", output)

#level 3
output = output[::-1]
print("level 2 output:", output)

#level 2
new = ""
i = 0
while i < len(output):
    toRead = int(output[i])
    sum = 0
    for j in range(1, toRead+1):
        sum += int(output[i+j])*10**(toRead-j)
    
    new += chr(sum)
    i += toRead+1

output = new
print("level 1 output:", output)

#level 1
print("raw flag: ", end="")
for i in output:
    if ord(i) > 99:
        print(chr(ord(i)-100), end="")
    else:
        print(chr(ord(i)+20), end="")