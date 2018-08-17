# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from OilAnalysis.settings import engine
from OilAnalysis.oilnews_settings import *
from OilAnalysis.sql import insert_values, gen_create_query
from OilAnalysis.spiders.oilnews import OilNewsSpider
from datetime import datetime


# Aug 16, 2018, 11:00 AM CDT


class OilNewsPipeline(object):
	__slots__ = "connection"

	def __init__(self):
		self.connection = engine.connect()

	def open_spider(self, spider):
		# create a new table if not exists
		if type(spider) == OilNewsSpider and not engine.has_table(oil_news_table_name):
			query = gen_create_query(oil_news_table_name, oil_news_column_types, oil_news_column_suffix)
			print(query)
			self.connection.execute(query)

	def close_spider(self, spider):
		if type(spider) == OilNewsSpider:
			self.connection.close()

	def process_item(self, item, spider):
		if type(spider) == OilNewsSpider:
			# format publish_time to standard datetime before insert
			date_str: str = item[col_date]
			date_str = date_str.replace("CDT", "CST")
			item[col_date] = datetime.strptime(date_str, "%b %d, %Y, %I:%M %p %Z")
			# insert into SQL
			insert_values(self.connection, oil_news_table_name, item)
			return item
		else:
			return item
