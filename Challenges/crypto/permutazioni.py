permutations = [
    [4, 1, 0, 3, 5, 2, 6, 7],
    [2, 6, 7, 0, 1, 3, 5, 4] ,
    [5, 2, 3, 7, 4, 0, 1, 6] ,
    [2, 6, 0, 3, 4, 7, 5, 1],
    [1, 2, 0, 4, 7, 5, 6, 3]
]

ciphred = [0,0,0,0,0,1,1,0]

def round_decrypt(fase, permutation):
    bits = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in permutation:
        bits[permutation[i]] = fase[i]

    return bits

def decrypt(bits):
    ROUNDS = len(permutations)

    for i in range(ROUNDS):
        bits = round_decrypt(bits, permutations[ROUNDS-i-1])

    result = "".join([str(i) for i in bits])
    print(result)

decrypt(ciphred)