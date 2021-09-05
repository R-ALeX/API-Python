import scrapy
from scrapy.http import HtmlResponse
from leruaMerlen.items import LeruamerlenItem
from scrapy.loader import ItemLoader
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/kuhonnye-stoly/']

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse,
                                 errback=self.errback_httpbin,
                                 dont_filter=True)

    def parse_httpbin(self, response):
        self.logger.info('Recieved response from {}'.format(response.url))

    def errback_httpbin(self, failure):
        # logs failures
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error("HttpError occurred on %s", response.url)

        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error("DNSLookupError occurred on %s", request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError occurred on %s", request.url)

    def parse(self, response: HtmlResponse):
        urls = response.xpath("//a[@data-qa='product-name']")
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for url in urls:
            yield response.follow(url, callback=self.parse_items)

    def parse_items(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruamerlenItem(), response=response)
        loader.add_xpath("name", "//h1/text()")
        loader.add_xpath("photos", "//img[@slot='thumbs']/@src")
        loader.add_xpath("description", "//section[@id='nav-description']//p/parent::div")
        options = {}
        for option in response.xpath("//div[@class='def-list__group']"):
            options[option.xpath("./dt/text()").get()] = option.xpath("./dd/text()").get()
        loader.add_value("options", options)
        loader.add_value("link", response.url)
        loader.add_xpath("price", "//span[@slot='price']/text()")
        yield loader.load_item()