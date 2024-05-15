finalResult = [ 0xaa, 0xa7, 0x7d, 0x74, 0x69, 0x81, 0x92, 0x62, 0xb8, 0x07, 0xcf, 0xa8, 0x9c, 0x07, 0x11, 0x63, 0x17, 0x77, 0x56, 0xd8, 0x79, 0xf1, 0x21, 0xac, 0x14, 0x82, 0x2a, 0x96, 0xaa, 0x73, 0x59, 0x9c, 0x29, 0xda, 0x92, 0x9b, 0xd0, 0x70, 0x73, 0xfc, 0xc3, 0x3f, 0x78, 0x40, 0xc6, 0x33, 0xfe, 0xef, 0x95, 0xde, 0xe4, 0xc7, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ]

def permutazione(stringa:str):
    
    v3 = []
    temp = []
    for i in range(52):
        v3.append(0)
        temp.append(0)
    
    v3[0] = 13 
    v3[1] = 25 
    v3[2] = 31 
    v3[3] = 10 
    v3[4] = 11 
    v3[5] = 15 
    v3[6] = 44 
    v3[7] = 51 
    v3[8] = 4 
    v3[9] = 46 
    v3[10] = 19 
    v3[11] = 28 
    v3[12] = 22 
    v3[13] = 50 
    v3[14] = 9 
    v3[15] = 30 
    v3[16] = 18 
    v3[17] = 20 
    v3[18] = 0 
    v3[19] = 26 
    v3[20] = 45 
    v3[21] = 42 
    v3[22] = 6 
    v3[23] = 48 
    v3[24] = 2 
    v3[25] = 39 
    v3[26] = 16 
    v3[27] = 7 
    v3[28] = 8 
    v3[29] = 24 
    v3[30] = 34 
    v3[31] = 17 
    v3[32] = 37 
    v3[33] = 36 
    v3[34] = 14 
    v3[35] = 3 
    v3[36] = 41 
    v3[37] = 33 
    v3[38] = 12 
    v3[39] = 23 
    v3[40] = 1 
    v3[41] = 40 
    v3[42] = 35 
    v3[43] = 49 
    v3[44] = 27 
    v3[45] = 21 
    v3[46] = 29 
    v3[47] = 43 
    v3[48] = 32 
    v3[49] = 47 
    v3[50] = 5 
    v3[51] = 38 
    
    for i in range(0x34):
        temp[i] = stringa[v3[i]]
    
    return temp

def xor(stringa:str):
    temp = stringa
    
    key = [ 0x9a, 0xf8, 0x1f, 0x2b, 0x1b, 0xe0, 0xab, 0x1f, 0xc3, 0x62, 0xfe, 0xda, 0xa8, 0x3f, 0x70, 0x3c, 0x75, 0x19, 0x30, 0xa0, 0x48, 0xc1, 0x54, 0xca, 0x75, 0xe6, 0x75, 0xa6, 0xde, 0x16, 0x6e, 0xef, 0x18, 0xed, 0xe6, 0xfc, 0xe4, 0x11, 0x06, 0xa3, 0xaf, 0x5e, 0x1d, 0x24, 0xf6, 0x5d, 0xca, 0x8e, 0xa3, 0xea, 0x96, 0xa5 ]
    for i in range(0x34):
        temp[i] ^= key[i]
        
    return temp

def back_xor(stringa):
    key = [ 0x9a, 0xf8, 0x1f, 0x2b, 0x1b, 0xe0, 0xab, 0x1f, 0xc3, 0x62, 0xfe, 0xda, 0xa8, 0x3f, 0x70, 0x3c, 0x75, 0x19, 0x30, 0xa0, 0x48, 0xc1, 0x54, 0xca, 0x75, 0xe6, 0x75, 0xa6, 0xde, 0x16, 0x6e, 0xef, 0x18, 0xed, 0xe6, 0xfc, 0xe4, 0x11, 0x06, 0xa3, 0xaf, 0x5e, 0x1d, 0x24, 0xf6, 0x5d, 0xca, 0x8e, 0xa3, 0xea, 0x96, 0xa5 ]
    temp = stringa
    
    for i in range(0x34):
        temp[i] ^= key[i]
        
    return temp

def back_permutazione(stringa):
    initialString = []
    v3 = []

    for i in range(52):
        v3.append(0)
        initialString.append(0)
    
    v3[0] = 13 
    v3[1] = 25 
    v3[2] = 31 
    v3[3] = 10 
    v3[4] = 11 
    v3[5] = 15 
    v3[6] = 44 
    v3[7] = 51 
    v3[8] = 4 
    v3[9] = 46 
    v3[10] = 19 
    v3[11] = 28 
    v3[12] = 22 
    v3[13] = 50 
    v3[14] = 9 
    v3[15] = 30 
    v3[16] = 18 
    v3[17] = 20 
    v3[18] = 0 
    v3[19] = 26 
    v3[20] = 45 
    v3[21] = 42 
    v3[22] = 6 
    v3[23] = 48 
    v3[24] = 2 
    v3[25] = 39 
    v3[26] = 16 
    v3[27] = 7 
    v3[28] = 8 
    v3[29] = 24 
    v3[30] = 34 
    v3[31] = 17 
    v3[32] = 37 
    v3[33] = 36 
    v3[34] = 14 
    v3[35] = 3 
    v3[36] = 41 
    v3[37] = 33 
    v3[38] = 12 
    v3[39] = 23 
    v3[40] = 1 
    v3[41] = 40 
    v3[42] = 35 
    v3[43] = 49 
    v3[44] = 27 
    v3[45] = 21 
    v3[46] = 29 
    v3[47] = 43 
    v3[48] = 32 
    v3[49] = 47 
    v3[50] = 5 
    v3[51] = 38 
    
    
    for i in range(0x34):
        initialString[v3[i]] = stringa[i]
        
    return initialString

temp = back_xor(finalResult)
for i in back_permutazione(temp):
    print(chr(i),end="")