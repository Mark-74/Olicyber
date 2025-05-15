from Crypto.Util.number import inverse, long_to_bytes
from gmpy2 import iroot

def crt(equations: list): # [[C, N], ...]
    M = 1
    for i in range(len(equations)):
        M = M * equations[i][1]                                             # M = N1 * N2 * ... * Nk (produttoria)
    
    Mi = [M // equations[i][1] for i in range(len(equations))]              # M / Ni
    Yi = [inverse(Mi[i], equations[i][1]) for i in range(len(equations))]   # Yi = Mi^(-1) mod Ni

    result = 0
    for i in range(len(equations)):
        result = (result + equations[i][0] * Mi[i] * Yi[i]) % M             # (result[i-1] + Yi * Mi * Ci) % M (sommatoria) 
    
    return result

def main():
    with open("challenge.txt", "r") as f:
        lines = f.readlines()
    
    equations = []
    for i in range(0, len(lines), 2):
        if i + 1 >= len(lines):
            break

        N = int(lines[i].strip().split("= ")[1])
        C = int(lines[i + 1].strip().split("= ")[1])

        equations.append([C, N])

    result = crt(equations)

    root = iroot(result, 17)
    print(long_to_bytes(root[0]).decode())

if __name__ == "__main__":
    main()

