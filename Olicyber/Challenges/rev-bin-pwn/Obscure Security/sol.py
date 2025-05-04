import sys

g4050 = 0x84ba7800
g4054 = 0x1438
g4058 = 0x10
g405C = 0x04
g4060 = 0x0a

def inv_cambia(v):
    for i in reversed(range(0, len(v), 2)):
        v[i+1] = (v[i+1] + 2*v[i]) & 0xff
        v[i] = (-(v[i] - v[i+1])) & 0xff
        v[i+1] = (v[i+1] - v[i]) & 0xff
        v[i] = (v[i] - v[i+1]) & 0xff

    return v

def inv_152E(v, int1, int2):
    for i in reversed(range(len(v))):
        tmp = v[i] - int2 + int1
        if tmp + g4050 & 0xff == int1:
            v[i] = tmp
    
    return v

def inv_1B4A(v1, v2):
    for i in reversed(range(len(v1))):
        for j in range(256):
            if v1[i] == (v2[i] & (~j)) | ((~v2[i]) & j):
                v1[i] = j
                break
    
    return v1
            
def inv_164e(v, shift):
    for i in reversed(range(len(v))):
        v[i] = (v[i] + i - shift) & 0xff
    
    return v
        
def inv_1491(v, _int):
    idx = 0
    i = _int - 1
    while i != -1:
        if v[idx] + 32 > 96 and v[idx] + 32 < 123:
            v[idx] += 32
            
        if i <= 0:
            i = -(i + 1)
        else:
            i = -(i - 1)
    
    return v

def inv_138E(v, length):
    i = 0
    while i < length:
        if i > 0:
            if v[i] + 32 > 96 and v[i] + 32 < 123:
                v[i] += 32
        else:
            if v[length - 1 + i] + 32 > 96 and v[length - 1 + i] + 32 < 123:
                v[length - 1 + i] += 32
            i-=1
        i = -i
    
    return v

def _1767(v, a2):
    n = len(v)
    k = a2 % n
    return v[k:] + v[:k]

def _1881(v, a2):
    n = len(v)
    k = a2 % n
    return v[-k:] + v[:-k]


output = [0xE7, 0x8E, 0x9A, 0x5C, 0xBA, 0xE0, 0xB5, 0x4E, 0x73, 0x5D, 0xCA, 0xDF, 0xDD, 0x75, 0x3D, 0xB6, 
        0xFE, 0x07, 0x9F, 0x92, 0x6F, 0xF4, 0x6B, 0xB0, 0x89, 0x0F, 0x28, 0x0D, 0x65, 0x64, 0x98, 0x33, 
        0xE3, 0xF9, 0x84, 0xC3, 0xB3, 0x8F, 0x50, 0x46]

g4020 = [0xBE, 0xC0, 0xC9, 0x76, 0xF5, 0xAB, 0xF6, 0x09, 0x56, 0x19, 0x85, 0xFD, 0xE1, 0x4D, 0x0E, 0x83, 
        0xE3, 0x46, 0xA8, 0xA6, 0x5B, 0xCB, 0x7C, 0x8B, 0xBE, 0x33, 0x1C, 0x24, 0x74, 0x51, 0xB3, 0x1B, 
        0xCB, 0xCA, 0x8F, 0xEC, 0x98, 0xBF, 0x78, 0x5B]

g4020 = inv_cambia(g4020)

output = inv_cambia(output)
output = inv_152E(output, 122, 64)
output = inv_1B4A(output, g4020)
output = inv_cambia(output)
output = inv_164e(output, g4050 & 0xff)
output = inv_1491(output, g4060)
tmp = inv_138E(output[g4060:], len(output[g4060:]))
output[g4060:] = tmp
output = _1767(output, g4058)

for i in range(len(output)):
    if output[i] == 0x24 - g4050 & 0xff:
        output[i] -= 0x73 - 0x24

output = inv_152E(output, 52, 97)
output = inv_152E(output, 51, 101)
output = inv_152E(output, 48, 111)
output = inv_152E(output, 55, 116)
output = inv_152E(output, 33, 105)
output = inv_152E(output, 95, 45)

output = _1881(output, g4058)

print('flag{' + "".join([chr(i) for i in output]) + '}')

if len(sys.argv) > 1 and sys.argv[1] == "CHECK":
    import subprocess
    
    out = subprocess.run(['./ObscureSecurity', "".join([chr(i) for i in output])], capture_output=True).stdout.strip().decode()
    print(out)
