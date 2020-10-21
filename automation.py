from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from operator import itemgetter
import time
import csv

global driver

driver = webdriver.Chrome()

USERNAME = '[YOUR USERNAME HERE]'
PASSWORD = '[YOUR PASSWORD HERE]'
SEARCHTYPE = 'LINK'     # 'NAME' or 'LINK'
CHECKEDU = ''
FILENAME = 'links.txt'

def login():
    username = driver.find_element_by_xpath('//*[@id="session_key"]')
    username.send_keys(USERNAME)
    password = driver.find_element_by_xpath('//*[@id="session_password"]')
    password.send_keys(PASSWORD)
    searchButton = driver.find_element_by_xpath('/html/body/main/section[1]/div[2]/form/button')
    searchButton.click()

def search(name):
    searchbox = None
    while True:
        try:
            searchbox = driver.find_element_by_xpath('//*[@id="ember16"]/input')
            searchbox.clear()
            searchbox.send_keys(name)
            searchbox.send_keys(Keys.RETURN)
            break
        except NoSuchElementException:
            continue
    timeend = time.time() + 3
    while time.time() < timeend:
        try:
            result = driver.find_element_by_css_selector('.search-result__result-link .ember-view')
            result.click()
            return True
        except NoSuchElementException:
            continue
    return False

def extract_edu(check=''):
    timeend = time.time() + 3
    edu = None
    while time.time() < timeend:
        try:
            edu = driver.find_element_by_xpath('//*[@id="education-section"]/ul')
            break
        except NoSuchElementException:
            continue
    if not edu:
        return False
    l = edu.find_elements_by_tag_name('li')
    check = False
    for i in l:
        if CHECKEDU in i.text:
            check = True
            break
    if check:
        college = l[0].find_elements_by_tag_name('h3')
        print(college[0].text + '\n')
        return college[0].text.strip(',')
    return False

def extract_name():
    timeend = time.time() + 3
    while time.time() < timeend:
        try:
            ul = driver.find_elements_by_tag_name('ul')[4]
            name = ul.find_elements_by_tag_name('li')[0]
            print(name.text)
            return name.text
        except NoSuchElementException:
            continue

def main():
    queries = []
    data = []
    with open(FILENAME) as f:
        queries = f.read().splitlines()
    driver.get('https://www.linkedin.com/')
    time.sleep(0.5)
    login()
    while True:
        try:
            if SEARCHTYPE == 'LINK':
                for i in queries:
                    driver.get(i)
                    name = extract_name()
                    edu = extract_edu(CHECKEDU)
                    if edu: data.append([ name, edu ])
                    time.sleep(0.5)
                break
            if SEARCHTYPE == 'NAME':
                for i in queries:
                    print(i)
                    if search(i):
                        edu = extract_edu(CHECKEDU)
                        if edu: data.append([ i, edu ])
                        time.sleep(1)
                break
        except KeyboardInterrupt:
            break
    data = sorted(data, key=itemgetter(0))
    with open('education.csv','w') as f:
        for i in data:
            f.write(','.join(i) + '\n')    

# main()