from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def run(spider_cls):
	process = CrawlerProcess(get_project_settings())
	process.crawl(spider_cls)
	process.start()
