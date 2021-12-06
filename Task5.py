from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
mvideo_goods = db.goods

def add_new(new):
    lnk = new['link']
    if mvideo_goods.count_documents({'link': lnk}) == 0:
        mvideo_goods.insert_one(new)

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get("https://www.mvideo.ru")

actions = ActionChains(driver)

while True:
    try:
        element = driver.find_element(By.XPATH, "//span[contains(text(),'В тренде')]")
        break
    except NoSuchElementException:
        actions.send_keys(Keys.PAGE_DOWN)
        actions.perform()
        time.sleep(3)
element.click()

in_trend = driver.find_element(By.XPATH, "//span[contains(text(),'В тренде')]//following::span")

names = driver.find_elements(By.XPATH, "//mvid-carousel[contains(@class, 'carusel')]//div[contains(@class, 'product-mini-card__name')]")
prices = driver.find_elements(By.XPATH, "//mvid-carousel[contains(@class, 'carusel')]//div[contains(@class, 'product-mini-card__price')]")

for item in range(len(names)):
    good = {}
    good['name'] = names[item].text
    good['price'] = int((prices[item].find_element(By.XPATH, ".//span[contains(@class,'price__main-value')]").text).replace(' ', ''))
    good['link'] = names[item].find_element(By.XPATH, ".//a").get_attribute('href')
    add_new(good)

for item in mvideo_goods.find({}):
    pprint(item)

driver.close()