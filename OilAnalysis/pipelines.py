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
    def target_tables(self):
        pass

    @property
    @abstractmethod
    def target_spider_name(self):
        pass

    def __init__(self):
        self.connection = engine.connect()

    def open_spider(self, spider):
        if spider.name == self.target_spider_name:
            for table_ddl in self.target_tables:
                self.initialize_table(table_ddl)

    def close_spider(self, spider):
        if spider.name == self.target_spider_name:
            self.connection.close()

    def process_item(self, item, spider):
        if spider.name != self.target_spider_name:
            return item
        item = self.pre_process_item(item)
        for ddl in self.target_tables:
            self.insert_item({k: v for k, v in item.items() if k in ddl.column_definitions}, ddl)
        return item

    def initialize_table(self, ddl):
        if not engine.has_table(ddl.table_name):
            self.connection.execute(ddl.create_query)

    def insert_item(self, item, ddl):
        self.connection.execute(ddl.insert_query(item))

    def close_spider(self):
        raise CloseSpider("")

    def pre_process_item(self, item):
        return item


class OilNewsPipeline(SQLExportPipeline):
    target_tables = [oil_news_DDL]
    target_spider_name = "oilnews"


class OilDailyPricePipeline(SQLExportPipeline):
    target_tables = [oil_price_categories_DDL, oil_price_indices_DDL, oil_price_DDL]
    target_spider_name = "oil_daily_price"
    cache_categories = {}
    cache_indices = {}

    def process_item(self, item, spider):
        if spider.name != self.target_spider_name:
            return item

        # try inserting new category name into table
        cat_name = item["category_name"]
        if cat_name not in self.cache_categories:
            category_id_query = "SELECT category_id FROM %s WHERE category_name='%s'" % (
                oil_price_categories_DDL.table_name, cat_name)
            res = list(self.connection.execute(category_id_query))
            if len(res) == 0:
                self.insert_item({"category_name": cat_name}, oil_price_categories_DDL)
                category_id = list(self.connection.execute(category_id_query))[0][0]
            else:
                category_id = res[0][0]
            self.cache_categories[cat_name] = category_id
        else:
            category_id = self.cache_categories[cat_name]

        # try inserting new index name into table
        index_name = item["index"]
        if index_name not in self.cache_indices:
            index_query = "SELECT index_id FROM %s WHERE index_name='%s'" % (
                oil_price_indices_DDL.table_name, index_name)
            res = list(self.connection.execute(index_query))
            if len(res) == 0:
                self.insert_item({"index_name": index_name, "category_id": category_id}, oil_price_indices_DDL)
                index_id = list(self.connection.execute(index_query))[0][0]
            else:
                index_id = res[0][0]
            self.cache_indices[index_name] = index_id
        else:
            index_id = self.cache_indices[index_name]

        # insert price into table
        self.insert_item({
            "index_id": index_id, "price": item["price"], "price_time": item["price_time"]
        }, oil_price_DDL)
        return item


if __name__ == "__main__":
    pass
