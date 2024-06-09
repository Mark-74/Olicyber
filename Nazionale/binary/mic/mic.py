xored_flag = b'\x33\x2d\x59\x32\x3f\x57\x33\x6c\x55\x0e\x20\x35\x79\x3e\x07\x58\x05\x31\x02\x3c\x27\x29\x39\x79\x7f\x07\x7c\x1a\x00\x3b\x73\x6c\x7a\x77\x0f\x37'
secret = [ 0x00, 0x01, 0x01, 0x01, 0x01, 0x03, 0x03, 0x01, 0x03, 0x03, 0x04, 0x05, 0x05, 0x00, 0x05, 0x02, 0x05, 0x03 ]
encrypted_key = 'AXQHFYKBG6KNE4DJCR7335XV3U8GDW1NZUI6'

def rotate_grille():
    new_grille = [0 for i in range(36)]
    v1 = 0
    for i in range(6):
        for j in reversed(range(0,6)):
            new_grille[6*j+i] = grille[v1]
            v1+=1
    return new_grille
    

grille = list(encrypted_key)
for i in reversed(range(4)):
    grille = rotate_grille()
    for j in reversed(range(9)):
        grille[6*secret[2*j] + secret[2*j+1]] = encrypted_key[i*9+j]
        print(len(grille), grille)
        
for i in grille:
    print(i, end='')