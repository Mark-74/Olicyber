import requests, json

s = requests.session()

response = s.post("http://web-11.challs.olicyber.it/login", json={"username": "admin", "password": "admin"})
flag = ""

for i in range(4):
    response = s.get("http://web-11.challs.olicyber.it/flag_piece", params={"csrf": response.json()["csrf"], "index": i})
    flag += response.json()["flag_piece"]

print(flag)
    
