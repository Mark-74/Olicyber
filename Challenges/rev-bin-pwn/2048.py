from pwn import *

conn = remote("2048.challs.olicyber.it", 10007)
print(conn.recvline())
print(conn.recvline())

for i in range(2048):
    operation = conn.recv(3).decode() #Pro = prodotto, #Div = divisione, #Som = somma, #Dif = differenza, Pot = potenza

    conn.recvuntil(' ') #discards the rest of the message until the numbers come out
    first = int(conn.recvuntil(' '))
    second = int(conn.recvuntil(' '))

    sending = 0
    
    if operation == "PRO":
        sending = first*second
    elif operation == "DIV":
        sending = first//second
    elif operation == "POT":
        sending = pow(first,second)
    elif operation == "SOM":
        sending = first+second
    elif operation == "DIF":
        sending = first-second

    print(str(first) + " " + str(second) + " " + operation + " " + str(sending))

    conn.sendline(str(sending))

print(conn.recv())