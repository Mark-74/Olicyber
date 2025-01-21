import requests

res = requests.get("http://sitogentile.challs.olicyber.it/talk")

for i in range(45):
    print(res.headers[f"X-Flag-{i}"], end="")