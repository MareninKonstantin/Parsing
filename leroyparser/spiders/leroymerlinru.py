import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem

class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@data-qa-pagination-item, 'right')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        name = response.xpath("//h1[@itemprop='name']/text()").get()
        photos = response.xpath("//img[@slot='thumbs']/@src").getall()
        url = response.url
        price = response.xpath("//uc-pdp-price-view[@class='primary-price']/span[@slot='price']/text()").get()
        print()
        yield LeroyparserItem(name=name, photos=photos, url=url, price=price)