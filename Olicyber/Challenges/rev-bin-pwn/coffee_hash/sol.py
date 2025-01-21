from z3 import *

psw = "630:624:622:612:609:624:623:610:624:624:567:631:638:639:658:593:546:605:607:585:648:636:635:704:702:687:687:682:629:699:633:639:634:637:578:622:620:617:606:615:568:633:589:587:645:639:653:654:633:634"

def check_password(input):
    hash_value = ""

    for var2 in range(len(input)): #hash has the same amount of chars as input
        var3 = 0

        for var4 in range(7):
            var3 += ord(input[(var2 + var4) % len(input)])

        hash_value += str(var3) if len(hash_value) == 0 else f":{var3}"

    return psw == hash_value

def main():
    enc = [int(i) for i in psw.split(':')]

    array = Array('array', IntSort(), IntSort())
    elements = [Int(f'array_{i}') for i in range(len(enc))]
    solver = Solver()

    for i in range(len(elements)):
        solver.add(And(
            elements[i] + elements[(i+1)%len(elements)] + elements[(i+2)%len(elements)] + elements[(i+3)%len(elements)] + elements[(i+4)%len(elements)] + elements[(i+5)%len(elements)] + elements[(i+6)%len(elements)] == enc[i],
            elements[i] > 0
        ))


    if solver.check() == sat:
        model = solver.model()
        array_values = [model[elem].as_long() for elem in elements]
        flag = ""
        for i in array_values:
            flag += chr(i)
        
        if(check_password(flag)):
            print("flag{" + flag + "}")
    else:
        print("No solution found")

if __name__ == "__main__":
    main()

