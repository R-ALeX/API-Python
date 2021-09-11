# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from parsingInstagram import settings


class ParsingPipeline:
    def __init__(self):
        connection = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
        self.mongobase = connection[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        collection.create_index([('user_id', 1), ('user_status', 1)], unique=True)
        collection.update({'$and': [{'user_id': item['user_id']}, {'user_status': item['user_status']}]},
                          {'$set': item}, upsert=True)
        return item


class ParsingPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            try:
                yield scrapy.Request(item['photo'])
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [_[1] for _ in results if _[0]]
        return item
