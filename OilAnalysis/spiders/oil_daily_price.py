# -*- coding: utf-8 -*-
import scrapy
from OilAnalysis.sqlsettings import *


class OilDailyPriceSpider(scrapy.Spider):
	name = 'oil_daily_price'
	allowed_domains = ['oilprice.com/oil-price-charts']
	start_urls = ['https://oilprice.com/oil-price-charts/']

	def parse(self, response):
		price_tables = response.css('div.oilprices__centercolumn table')
		for table in price_tables:
			# get index category name
			table_name = table.css('th::text').extract_first()
			body = table.css('tbody.row_holder tr')
			for row in body:
				# get time entry from two sources
				time = row.css('td.last_updated::attr("data-stamp")').extract_first()
				if time == "":
					time = row.css('td.last_updated::text').extract_first()
				# if time is not get, it's more like a subtitle table row, so skip it
				if not time:
					continue

				yield {
					col_price_category: table_name,
					col_price_index_name: row.css('td::text').extract_first(),
					col_price_last: row.css('td.last_price::text').extract_first(),
					col_price_abs_change: row.css('td.change_up::text,td.change_down::text').extract_first(),
					col_price_per_change: row.css(
						'td.change_up_percent::text,td.change_down_percent::text').extract_first(),
					col_price_update_time: time
				}
