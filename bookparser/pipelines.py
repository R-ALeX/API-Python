# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


from pymongo import MongoClient
from bookparser import settings


class MongoDBPipeline(object):
    def __init__(self):
        settings.MONGODB_HOST
        connection = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
        db = connection[settings.MONGODB_DATABASE]
        self.collection = db[settings.MONGODB_COLLECTION]

class BookparserPipeline:
    def process_item(self, item, spider):
        self.collection.insert(item)
        return item
