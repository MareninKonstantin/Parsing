import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/python/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@title='Следующая']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[contains(@class, 'card-column')]//a[@class='cover']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        link = response.url
        name = response.xpath('//h1/text()').get()
        author = response.xpath('//a[@data-event-label="author"]/text()').get()
        price = response.xpath('//span[@class="buying-priceold-val-number"]/text()').get()
        price_discount = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()
        rate = response.xpath('//div[@id="rate"]/text()').get()
        item = BookparserItem(link=link, name=name, author=author, price=price, price_discount=price_discount, rate=rate)
        yield item