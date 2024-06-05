from flask import Flask, Response, request
from z3 import *

app = Flask(__name__)

@app.route("/")
def hello_world():
    token = request.headers.get('User-Agent').encode()
    print(token)
    secret = [87, 71, 179, 169, 154, 69, 91, 217, 185, 174, 69, 44, 63, 223, 237, 47, 20, 62, 215, 47, 3, 89, 54, 255, 80, 239, 181, 130, 78, 57, 186, 91]
    cnc = []
    
    for i in range(30):
        s = Solver()

        A1=BitVec('A1', 8)
        B1=BitVec('B1', 8)
        A2=BitVec('A2', 8)
        B2=BitVec('B2', 8)
        
        if i != 0:
            s.add(B1 == x)
            
        s.add(A1 == int(token[i]))
        s.add(A2 == int(token[i+1]))
        s.add((A1 ^ B1) + (A2 ^ B2) % 256 == secret[i])
        
        if s.check() == sat:
            cnc.append(s.model()[B1].as_long())
            x = s.model()[B2]
            
            if i == 30:
                cnc.append(s.model()[B2].as_long())
    
    CnC = ''.join([chr(i) for i in cnc])
    response = Response("<p>Hello, World!</p>", status=200, headers={"Server-Type":"Frontdoor-Server-1.0", "C&c": CnC})
    return response

@app.route("/command.txt")
def command():
    print(request.headers.get('Flag'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)