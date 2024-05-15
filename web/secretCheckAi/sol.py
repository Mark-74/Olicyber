import base64

data = 'aXQwNG5kXzExbHM0X3ZuXzMzdmQzMXJzX190dGhuMzNfMXNsMGNse3VDdEUxUzBBblQhSX0='
value = base64.decodebytes(data.encode()).decode()
result = [ " " ]*len(value)

i = 0
j = len(value)-1
k = False

while j-i >= 0:
    if k:
        result[i] = value[j-i]
        i+=1
        k=False
    else:
        result[j] = value[j-i]
        j-=1
        k=True
        
for i in result:
    print(i,end="")