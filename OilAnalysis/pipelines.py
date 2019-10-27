# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from BackEnd.tableddl import *
from abc import ABC, abstractmethod
from sqlalchemy.exc import IntegrityError
from BackEnd.settings import engine


class SQLPipeline(ABC):
    __slots__ = "connection"
    engine = engine

    @property
    @abstractmethod
    def target_spider(self) -> str:
        pass

    @property
    @abstractmethod
    def table(self) -> Table:
        pass

    def __init__(self):
        self.connection = None

    def open_spider(self, spider):
        if self.target_spider == spider.name:
            self.connection = self.engine.connect()
            if not self.engine.has_table(self.table.name):
                self.table.create(self.engine)

    def close_spider(self, spider):
        if self.target_spider == spider.name:
            self.connection.close()

    def process_item(self, item, spider):
        if self.target_spider == spider.name:
            return self._process_target_item(item)
        else:
            return item

    @abstractmethod
    def _process_target_item(self, item):
        pass


# retrieve id(or any other) of a certain value from a SQL table, then add it to item
# if value if not found, insert that value
class SQLItemJoinPipeline(SQLPipeline, ABC):
    __slots__ = "value_cache"

    @property
    @abstractmethod
    def search_column_name(self) -> str:
        pass

    @property
    @abstractmethod
    def retrieve_column_name(self) -> str:
        pass

    @property
    def search_column(self) -> Column:
        return self.table.columns[self.search_column_name]

    @property
    def retrieve_column(self) -> Column:
        return self.table.columns[self.retrieve_column_name]

    def __init__(self):
        super().__init__()
        self.value_cache = {}

    def _process_target_item(self, item):
        val = item[self.search_column_name]
        if val not in self.value_cache:
            # try retrieve value from table by select query
            query = self.table.select(self.retrieve_column).where(self.search_column == val)
            res = list(self.connection.execute(query))
            if len(res) == 0:
                # not matching value, so insert one
                self.connection.execute(self.table.insert().values({self.search_column_name: val}))
                retrieved_id = list(self.connection.execute(query))[0][0]
            else:
                retrieved_id = res[0][0]
            item[self.retrieve_column_name] = retrieved_id
        else:
            # directly add value from cache
            item[self.retrieve_column_name] = self.value_cache[val]
        return item


class SQLExportPipeline(SQLPipeline, ABC):
    def _process_target_item(self, item):
        try:
            used_item = {k: v for k, v in item.items() if k in self.table.columns}
            query = self.table.insert().values(used_item)
            self.connection.execute(query)
            return item
        except IntegrityError:
            return item


class OilNewsPipeline(SQLExportPipeline):
    table = oil_news_table
    target_spider = "oilnews"


class OilDailyPricePipeline(SQLExportPipeline):
    table = oil_price_table
    target_spider = "oil_daily_price"


class CategoryJoinPipeline(SQLItemJoinPipeline):
    search_column_name: str = "category_name"
    retrieve_column_name: str = "category_id"
    target_spider: str = "oil_daily_price"
    table: Table = oil_price_categories_table


class IndexJoinPipeline(SQLItemJoinPipeline):
    search_column_name: str = "index_name"
    retrieve_column_name: str = "index_id"
    target_spider: str = "oil_daily_price"
    table: Table = oil_price_indices_table
