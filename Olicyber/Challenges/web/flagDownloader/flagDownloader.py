#/bin/python3
import requests

flag = ""

p = "http://flagdownloader.challs.olicyber.it/download/flag/"
for i in range(30):
    if i == 0: n = "0"
    else: 
        response = page.json()
        flag += response['c']
        n = response['n']
    page = requests.get(p + n)

print(flag)