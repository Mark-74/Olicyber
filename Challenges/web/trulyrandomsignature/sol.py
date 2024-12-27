#!/usr/bin/env python3.8
import requests, time, string, random, hmac, hashlib
from datetime import datetime, timedelta

def sign(text, key):
  textAsBytes = bytes(text, encoding='ascii')
  keyAsBytes  = bytes(key, encoding='ascii')
  signature = hmac.new(keyAsBytes, textAsBytes, hashlib.sha256)
  return signature.hexdigest()

url = "http://trulyrandomsignature.challs.olicyber.it/"

response = requests.get(url)
uptime = int(response.headers['X-Uptime'])

current_time = time.time()
start_time = current_time - uptime
seed_time = datetime.utcfromtimestamp(start_time)
seed = seed_time.strftime('%Y-%m-%d %H:%M:%S')

print(f'Seed: {seed}')
random.seed(seed)

letters = string.ascii_lowercase
result_str = ''.join(random.choice(letters) for i in range(32))

signature = sign("admin", result_str)

print(f'Signature: {signature}')

#if it doesn't work first time, try again because the seed is retrieved from the time which is float and is rounded to the nearest second
response = requests.get(url + "/admin", cookies={"user": "admin", "signature": signature})
print(response.text)