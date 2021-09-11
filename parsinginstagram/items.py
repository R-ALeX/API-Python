# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParsinginstagramItem(scrapy.Item):
    user_id = scrapy.Field()
    username = scrapy.Field()
    picture = scrapy.Field()
    likes = scrapy.Field()
    post_data = scrapy.Field()
    from_username = scrapy.Field()
