from pwn import xor

def c1(_input):
    return 80 * (_input + 7) + 6

def c2(_input):
    return 12 * _input + 15

def c3(_input):
    return 4 * _input + 15

def c4(_input):
    return 6 * (2 * (_input + 16) + 8)

def c5(_input):
    return 5400 * (_input + 5)

def c6(_input):
    return 8 * (_input + 6) + 25

def c7(_input):
    return 7 * (_input + 2) + 6

def c8(_input):
    return 6 * (_input + 10) + 14

def c9(_input):
    return 9 * (9 * (_input + 6) + 10)

def c10(_input):
    return 8 * (_input + 9) + 8

def c11(_input):
    return 784 * _input

def c12(_input):
    return 5 * (9 * (_input + 1) + 3) + 6

def c13(_input):
    return 576 * _input + 13

def c14(_input):
    return 4 * (252 * _input + 6)

def c15(_input):
    return 2916 * _input

def c16(_input):
    return 432 * (_input + 7)

def c17(_input):
    return 50 * (_input + 4) + 3

def c18(_input):
    return 8 * _input + 19

def c19(_input):
    return 9 * (50 * _input + 10) + 9

def c20(_input):
    return 80 * (_input + 4) + 2

def c21(_input):
    return 6 * (_input + 10) + 16

def c22(_input):
    return 180 * (_input + 8)

def c23(_input):
    return 20 * (_input + 2) + 9

def c24(_input):
    return 10 * (_input + 20)

def c25(_input):
    return 4 * (6 * (_input + 5) + 7)

def c26(_input):
    return 180 * (_input + 5) + 2

def c27(_input):
    return 21 * (9 * _input + 7) + 9

def c28(_input):
    return 8 * (_input + 36)

def c29(_input):
    return 2 * _input + 9

def c30(_input):
    return 5 * (16 * (_input + 2) + 7)

def c31(_input):
    return 7 * (5 * _input + 6) + 9

def c32(_input):
    return _input + 19

def decrypt(p0: str) -> str:

    ref = "NUKRPFUFALOXYLJUDYRDJMXHMWQW".upper()
    out = []
    local_0 = 0
    p0_len = len(p0)
    for c1 in ref:
        c2 = p0[local_0]
        val = (((ord(c1) - ord(c2)) + 0x1A) % 0x1A) + ord('A')
        out.append(chr(val))
        local_0 = (local_0 + 1) % p0_len

    return ''.join(out)

results = [6326, 2259, 455, 1848, 275400, 745, 1714, 1076, 12645, 2120, 153664, 10371, 37453, 203640, 691092, 36288, 753, 2011, 59949, 18082, 538, 12420, 2529, 1130, 6076, 11702, 47217, 1056, 207, 11315, 2676, 261]

if __name__ == "__main__":

    password = []
    for i in range(32):    
        f = eval("c"+str(i+1))
        for j in range(256):        
            if f(j) == results[i]:            
                password.append(j)
                    
    with open("enc_payload.enc", "rb") as f:
        enc = f.read()
        
    with open("dec_payload", "wb") as f:
        f.write(xor(enc, bytes(password)))
        print("Decompile dec_payload, it's a dex file")

    print("ptm{" + decrypt("EASYPEASY") + "}")
    
