from bs4 import *
import requests

def get_html(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup

already_fetched = []

queue = []
queue.append("")
sp = 0

baseUrl = "http://web-16.challs.olicyber.it"
found = False

while(not found):
    pagina = get_html(baseUrl + queue[sp])
    a_list = pagina.find_all('a')

    for href in a_list:
        if href["href"] in already_fetched: continue
        else:
            queue.append(href["href"]) # fa append solo di /page?... mettere baseUrl nel fetch
            already_fetched.append(href["href"])
            h1 = pagina.find_all("h1")
            if "flag" in h1[0].get_text():
                print(h1)
                found = True
                break
            else: print("not found in " + href["href"])
    sp += 1
