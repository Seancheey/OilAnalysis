# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from OilAnalysis.spiders.oilnews import OilNewsSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
	process = CrawlerProcess(get_project_settings())
	process.crawl(OilNewsSpider)
	process.start()


if __name__ == "__main__":
	main()
