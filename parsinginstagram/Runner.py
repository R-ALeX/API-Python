from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from parsingInstagram.spiders.inst import InstSpider
from parsingInstagram.spiders.instfollowers import InstagramfollowersSpider
from parsingInstagram import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    #process.crawl(InstSpider)
    process.crawl(InstagramfollowersSpider)
    process.start()