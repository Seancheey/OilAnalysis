from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet.error import DNSLookupError
from datetime import datetime


def run(spider_cls):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_cls)
    try:
        process.start()
    except DNSLookupError:
        print("Error At", datetime.now(), ": DNS lookup failed")
