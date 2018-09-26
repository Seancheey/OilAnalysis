# -*- coding: utf-8 -*-
import scrapy
from OilAnalysis.runspider import run


class OilStockSpider(scrapy.Spider):
    name = 'oil_stock'
    allowed_domains = ['www.investing.com/economic-calendar/api-weekly-crude-stock-656']
    start_urls = ['http://www.investing.com/economic-calendar/api-weekly-crude-stock-656/']

    def parse(self, response):
        # TODO parse each row into {stock_name, volume, update_time} :D
        print(response.css("table.ecHistoryTbl"))
        yield {
            response.css("table.ecHistoryTbl").extract_first()
        }


if __name__ == "__main__":
    run(OilStockSpider)
