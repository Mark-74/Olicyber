from pwn import remote, context

def solve(stato: list, bottoni: list) -> str:
    output = ""
    print(bottoni, stato)
    for i in range(len(bottoni)):

        flag = False
        for j in bottoni[i]:
            while stato[j] < 5:
                stato[j] += 1
                if not flag:
                    output += str(i+1) + ' '
            flag = True

    print(output)
    return output[:-1]

r = remote("test.challs.olicyber.it", 15004)
context.log_level = 'debug'
r.recvlines(20)

livello = r.recvline()
while livello.startswith(b"Livello"):
    stato = [int(_) for _ in r.recvline(False).decode().split()]
    mosse = []
    while True:
        s = r.recvline(False).decode()
        if s == "":
            break
        mosse.append(["ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(_) for _ in s.split()])
    res = solve(stato, mosse)
    r.sendline(res)
    r.recvlines(2)
    livello = r.recvline()
