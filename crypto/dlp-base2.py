h = 132768
b = 2
p = 49398895282787034671303842596545890841

exp = 0

for i in range(100):
    if p // 2**i == 1:
        exp = i
        break
    
while True:
    if pow(b, exp, p) == h:
        print(i)
        break
    else: exp += 1