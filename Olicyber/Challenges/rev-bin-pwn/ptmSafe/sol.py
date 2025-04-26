from gmpy2 import iroot

flag = ['p','t','m','{', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '}']

flag[4] = chr(30 ^ ord(flag[0]))
flag[5] = '0'
flag[6] = chr(0x13e ^ 3*ord(flag[4]))
flag[7] = '_'
flag[9] = chr(iroot(0x1B000, 3)[0])
flag[12] =  chr(0xd0 // 4)
flag[13] = 'f'
flag[8] = chr(ord('G') ^ ord(flag[12]))

for i in range(256):
    if not chr(i).isprintable():
        continue
    
    if i * ord(flag[8]) <= 13229:
        flag[11] = chr(i)
    
flag[10] = chr(ord(flag[4]) + 100 - ord(flag[11]))

for i in range(256):
    if not chr(i).isprintable():
        continue
    
    tmp = 0
    
    flag[14] = chr(i)
    for c in flag:
        tmp ^= ord(c)
    
    if tmp == 0x14:
        break
    
print(''.join(flag))