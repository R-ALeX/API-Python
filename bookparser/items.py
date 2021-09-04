# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    book_name = scrapy.Field()
    book_url = scrapy.Field()
    book_author = scrapy.Field()
    book_price = scrapy.Field()
    book_price_discount = scrapy.Field()
    book_rating = scrapy.Field()
    pass
