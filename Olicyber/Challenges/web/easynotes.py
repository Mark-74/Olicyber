import requests, json

print(json.loads(requests.get('http://easynotes.challs.olicyber.it/api/note/1').text)['content'])
