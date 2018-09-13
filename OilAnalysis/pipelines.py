# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from OilAnalysis.settings import engine
from OilAnalysis.tableddl import *
from abc import ABC, abstractmethod
from scrapy.exceptions import CloseSpider


# Aug 16, 2018, 11:00 AM CDT

class SQLExportPipeline(ABC):
    __slots__ = "connection"

    @property
    @abstractmethod
    def table_ddl(self) -> TableDDL:
        pass

    @property
    @abstractmethod
    def target_spider_name(self):
        pass

    def __init__(self):
        self.connection = engine.connect()

    def open_spider(self, spider):
        if spider.name == self.target_spider_name and not engine.has_table(self.table_ddl.table_name):
            self.connection.execute(self.table_ddl.create_query)

    def close_spider(self, spider):
        if spider.name == self.target_spider_name:
            self.connection.close()

    def process_item(self, item, spider):
        if spider.name != self.target_spider_name:
            return item
        item = self.pre_process_item(item)
        self.connection.execute(self.table_ddl.insert_query(item))
        return item

    def close_spider(self):
        raise CloseSpider("")

    @abstractmethod
    def pre_process_item(self, item):
        return item


class OilNewsPipeline(SQLExportPipeline):
    table_ddl = oil_news_DDL
    target_spider_name = "oilnews"

    def pre_process_item(self, item):
        return item


class OilDailyPricePipeline(SQLExportPipeline):
    table_ddl = oil_price_DDL
    target_spider_name = "oil_daily_price"

    def pre_process_item(self, item):
        # format last update
        return item
