# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class LeroyparserItem(scrapy.Item):
    name = scrapy.Field()
    photos = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
