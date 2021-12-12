# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class BookparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books

    def process_item(self, item, spider):
        item['name'] = self.name_proc(item['name'])
        item['price'] = self.price_proc(item['price'])
        item['price_discount'] = self.price_discount_proc(item['price_discount'])
        item['rate'] = self.rate_proc(item['rate'])

        collection = self.mongobase[spider.name]
        if collection.count_documents({'link': item['link']}) == 0:
            collection.insert_one(item)
        return item

    @staticmethod
    def name_proc(name):
        try:
            name = name.split(':')[1][1:]
        finally:
            return name

    @staticmethod
    def price_proc(price):
        try:
            price = int(price)
        except:
            price = None
        finally:
            return price

    @staticmethod
    def price_discount_proc(price_discount):
        try:
            price_discount = int(price_discount)
        except:
            price_discount = None
        finally:
            return price_discount

    @staticmethod
    def rate_proc(rate):
        try:
            rate = float(rate)
        except:
            rate = None
        finally:
            return rate