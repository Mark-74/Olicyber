with open("output.txt", "r") as f:
    enc = f.read()

counter, i = 0, 0
cur = enc[0]
while True:
    try:
        if enc[i] == cur:
            counter+=1
        else:
            print(chr(counter),end="")
            counter=1
            cur = enc[i]
        i+=1
    except:
        break

print("}\n")

