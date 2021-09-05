from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leruaMerlen.spiders.lerua import LeruaSpider
from leruaMerlen import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeruaSpider)
    process.start()