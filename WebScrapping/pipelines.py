# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# original code template
from itemadapter import ItemAdapter


class WebscrappingPipeline:
    def process_item(self, item, spider):
        return item