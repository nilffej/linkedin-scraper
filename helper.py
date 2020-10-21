from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from operator import itemgetter
import time

USERNAME = '[YOUR USERNAME HERE]'
PASSWORD = '[YOUR PASSWORD HERE]'
SEARCHTYPE = 'LINK'     # 'NAME' or 'LINK'

# CUTS EVERY OTHER LINE #

def parse():
    temp = []
    with open('text.txt') as f:
        temp = f.readlines()
    with open('names.txt','w') as f:
        for i in range(len(temp)//2):
            f.write('{}'.format(temp[2*i]))

def remove_stuy():
    temp = []
    with open('education.csv') as f:
        temp = f.readlines()
    with open('processed.csv','w') as f:
        for item in temp:
            if 'Stuyvesant' not in item : f.write(item)

def sortlist():
    temp = []
    out = []
    stuylist = []
    with open('education.csv') as f:
        temp = f.readlines()
    for i in temp:
        x = i.split(',')
        if 'Stuyvesant' in x[1] : stuylist.append(x)
        else : out.append(x)
    out = sorted(out, key=itemgetter(0))
    stuylist = sorted(stuylist, key=itemgetter(0))
    with open('processed.csv','w') as f:
        for i in out:
            f.write('{}'.format(','.join(i)))
        for i in stuylist:
            f.write('{}'.format(','.join(i)))


def getuserlist():
    driver = webdriver.Chrome()
    driver.get('https://www.linkedin.com/')

    username = driver.find_element_by_xpath('//*[@id="session_key"]')
    username.send_keys(USERNAME)
    password = driver.find_element_by_xpath('//*[@id="session_password"]')
    password.send_keys(PASSWORD)
    searchButton = driver.find_element_by_xpath('/html/body/main/section[1]/div[2]/form/button')
    searchButton.click()

    driver.get('https://www.linkedin.com/groups/12076764/members/')
    time.sleep(1)

    oldheight = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        height = driver.execute_script("return document.body.scrollHeight")
        if height == oldheight:
            break
        oldheight = height
    members = driver.find_element_by_xpath('//*[@id="ember60-a11y"]')
    l = []
    if SEARCHTYPE == 'NAME':
        l = members.find_elements_by_css_selector('.artdeco-entity-lockup__title')
    if SEARCHTYPE == 'LINK':
        l = members.find_elements_by_css_selector('.ui-entity-action-row__link')
    with open('names.txt','w') as f:
        for item in l:
            if SEARCHTYPE == 'NAME':
                f.write(item.text + '\n')
            if SEARCHTYPE == 'LINK':
                f.write(item.get_attribute('href') + '\n')
            
# parse()
# getuserlist()
# remove_stuy()
sortlist()