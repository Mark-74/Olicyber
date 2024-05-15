from bs4 import *
import requests
from selenium import webdriver
import logging
import selenium.webdriver
import selenium.webdriver.firefox.service

    
headers={'Content-Type': 'application/x-www-form-urlencoded'}
url = "http://infinite.challs.olicyber.it/"


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

firefox_bin = "/snap/firefox/current/usr/lib/firefox/firefox"
firefoxdriver_bin = "/snap/firefox/current/usr/lib/firefox/geckodriver"

options = selenium.webdriver.firefox.options.Options()
options.add_argument('--headless')
options.binary_location = firefox_bin

service = selenium.webdriver.firefox.service.Service(executable_path=firefoxdriver_bin)

driver = selenium.webdriver.Firefox(service=service, options=options)
driver.get(url)

print(driver.page_source)

  
while True:
        
    page = BeautifulSoup(driver.page_source, 'html.parser')
        
    title = page.find("title").text 
    req = page.find("p").text 
        
    if title == "MATH TEST": #it's always a sum
        number1 = req[10:]
        for i in range(len(number1)):
            if number1[i] == ' ':
                number1 = number1[:i]
                break
        number2 = req[10+len(number1)+3:]
        for i in range(len(number2)):
            if number2[i] == '?':
                number2 = number2[:i]
                break
            
        result = int(number1)+int(number2)
        print(number1, number2, result)
            
        driver.find_element(value='sum').send_keys(str(result))
        driver.find_element(by='xpath', value="//input[@type='submit' and @value='Submit']").click()
            
    elif title == "GRAMMAR TEST": #how many letters in word
        letter = req[8]
        word = req[33:len(req)-2]
            
        count = 0
        for i in word:
            if i == letter:
                count+=1
                    
        print(word, letter, count)

        driver.find_element(value='letter').send_keys(str(count))
        driver.find_element(by='xpath', value="//input[@type='submit' and @value='Submit']").click()
            
    elif title == "ART TEST": #the color matches the id of the button to press
        color = req[28:len(req)-1]
        print(color)
        
        driver.find_element(value=color).click()
        
    else: #flag found
        print(page)
        break