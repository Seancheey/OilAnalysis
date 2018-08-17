# -*- coding: utf-8 -*-
import scrapy


class OilDailyPriceSpider(scrapy.Spider):
	name = 'oil_daily_price'
	allowed_domains = ['https://oilprice.com/oil-price-charts']
	start_urls = ['http://https://oilprice.com/oil-price-charts/']

	def parse(self, response):
		pass
