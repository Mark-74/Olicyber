from z3 import *

secret = [87, 71, 179, 169, 154, 69, 91, 217, 185, 174, 69, 44, 63, 223, 237, 47, 20, 62, 215, 47, 3, 89, 54, 255, 80, 239, 181, 130, 78, 57, 186, 91]
token = []

for i in range(31):
    token.append(i)
    
    x = 0
for i in range(30):
    s = Solver()

    A1=BitVec('A1', 8)
    B1=BitVec('B1', 8)
    A2=BitVec('A2', 8)
    B2=BitVec('B2', 8)
    
    if i is not 0:
        s.add(B1 == x)
        
    s.add(A1 == int(token[i]))
    s.add(A2 == int(token[i+1]))
    s.add((A1 ^ B1) + (A2 ^ B2) % 256 == secret[i])
    
    if s.check() == sat:
        print(s.model())
        x = s.model()[B2]