import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

class LeroyparserPipeline:
    def process_item(self, item, spider):
        print()
        return item

class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print()
        pass
        # if item['photos']:
        #     for img in item['photos']:
        #         try:
        #             yield scrapy.Request(img)
        #         except Exception as e:
        #             print(e)