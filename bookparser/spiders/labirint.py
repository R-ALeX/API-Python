import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/best/',
                  'https://www.labirint.ru/books/']

    def parse(self, response: HtmlResponse, my_url='https://www.labirint.ru'):
        urls = list(map(my_url.__add__, response.xpath("//a[@class='cover']/@href").getall()))
        next_page = my_url + response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for url in urls:
            yield response.follow(url, callback=self.books_parse)

    def books_parse(self, response: HtmlResponse):
        book_name = response.xpath("//h1/text()").get()
        book_url = response.url
        book_author = response.xpath("//a[@data-event-label='author']/text()").get()
        book_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        book_price_discount = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        book_rating = response.xpath("//div[@id='rate']/text()").get()
        item = BookparserItem(book_name=book_name, book_url=book_url,book_author=book_author,book_price=book_price,book_price_discount=book_price_discount,book_rating=book_rating)
        yield item