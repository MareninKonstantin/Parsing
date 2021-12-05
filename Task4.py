from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['lenta_news']
news_mongo = db.news
#news_mongo.delete_many({})

def add_new(new):
    lnk = new['link']
    if news_mongo.count_documents({'link': lnk}) == 0:
        news_mongo.insert_one(new)

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
url = 'https://lenta.ru'

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

links = dom.xpath("//div[contains(@class,'b-yellow-box__wrap')]//@href")

for link in links:
    response = requests.get(url+link, headers=header)
    dom = html.fromstring(response.text)

    new = {}

    source = url
    name = dom.xpath("//h1[@class='b-topic__title']/text()")[0].replace('\xa0', ' ')
    new['source'] = source
    new['name'] = name
    new['link'] = url+link
    new['datetime'] = dom.xpath("//time[@class='g-date']/text()")[0][1:]

    add_new(new)

for new in news_mongo.find({}):
    pprint(new)

