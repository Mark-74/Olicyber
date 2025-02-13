import random

#output from cifrario_a_caso.py
enc = bytes.fromhex('088596df93697e62d71cb143352ccb45be15463219c6cc917f9be83c1aa1f7d0217b4586c1058009')

for i in range(256):
    random.seed(i)
    
    flag = ''
    for c in enc:
        flag += chr(c ^ random.randint(0, 255))
    
    if 'flag{' in flag:
        print(flag)
        break