from pwn import *
import json
import base64
from Crypto.Util.number import bytes_to_long, long_to_bytes

conn = remote("based.challs.olicyber.it", 10600)
limit = "\n\n".encode()

while True:
    
    #skippo le prime linee
    try:
        print(conn.recvuntil(limit))
    except:
        print(conn.recv())
        break
    
    temp = conn.recvline()
    print(temp)
    req = temp[16:].decode()
    
    mes = conn.recvline().decode()
    try:
        mes = json.loads(mes)
    except:
        print(mes)
        break
    
    answer = ""
    if req[0] == 'd': #convertire da ...
        req = req[3:]
        if req[0] == "e": #esadecimale
            answer = int(mes["message"], 16)
            bytes = long_to_bytes(answer)
            answer = bytes.decode()
            
        elif req[0:2] == "bi": #binario
            numero = int(mes["message"], 2)
            answer = long_to_bytes(numero).decode()
            
        else: #base64
            bytes = mes["message"].encode()
            answer = base64.b64decode(bytes).decode()
            
    else: #converti a ...
        req = req[2:]
        if req[0] == "e": #esadecimale
            bytes = mes["message"].encode()
            answer = hex(bytes_to_long(bytes))[2:]
            
        elif req[0:2] == "bi": #binario
            bytes = mes["message"].encode()
            answer = ''.join(format(byte, '08b') for byte in bytes)
            while answer[0] == "0":
                answer = answer[1:]
            
        else: #base64
            bytes = base64.b64encode(mes["message"].encode())
            answer = bytes.decode()
            
    answer = json.dumps({"answer": answer}, indent=0).replace("\n", "")
    conn.sendline(answer)
    print(conn.recv())