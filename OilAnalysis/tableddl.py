from datetime import datetime
from sqlalchemy import MetaData
from sqlalchemy.sql import text
from sqlalchemy.schema import Table, Column, UniqueConstraint, ForeignKey
from sqlalchemy.types import VARCHAR, TEXT, INTEGER, TIMESTAMP, DATE, DATETIME, FLOAT
from OilAnalysis.settings import test_engine, engine

meta = MetaData()
meta.bind = engine

# class TableDDL:
#     __slots__ = "table_name", "column_definitions", "constraints"
#
#     def __init__(self, table_name, column_definitions, constraints=None):
#         self.table_name = table_name
#         self.column_definitions = column_definitions
#         self.constraints = constraints if constraints is not None else []
#
#     @property
#     def column_types(self):
#         return {col_name: (definition[0] if type(definition) == tuple else definition) for col_name, definition in
#                 self.column_definitions.items()}
#
#     @property
#     def column_suffix(self):
#         return {col_name: (definition[1] if type(definition) == tuple else "") for col_name, definition in
#                 self.column_definitions.items()}
#
#     @property
#     def create_query(self):
#         entries = ["%s %s %s" % (c, t, self.column_suffix[c] if c in self.column_suffix else "") for c, t in
#                    self.column_types.items()]
#         constraint = ",\n\t" + ",\n\t".join(self.constraints) if len(self.constraints) else ""
#         return "CREATE TABLE IF NOT EXISTS %s(\n\t%s%s\n);" % (self.table_name, ",\n\t".join(entries), constraint)
#
#     def insert_query(self, values: dict):
#         for col_name in values.keys():
#             if col_name not in self.column_definitions:
#                 raise KeyError("column name: %s is not found in DDL of %s" % (col_name, self.table_name))
#         columns = ",".join(values.keys())
#         col_values = ",".join(
#             [str(value) if type(value) not in [datetime, str] else "'%s'" % value for value in values.values()]
#         )
#         return "INSERT INTO %s(%s) VALUES (%s);" % (self.table_name, columns, col_values)
#
#     def __str__(self):
#         return self.create_query


oil_news_table = Table(
    "oil_news", meta,
    Column("id", INTEGER, primary_key=True, autoincrement=True),
    Column("title", VARCHAR(100), nullable=False),
    Column("publish_date", DATETIME, nullable=False),
    Column("author", VARCHAR(100)),
    Column("content", TEXT, nullable=False),
    Column("reference", VARCHAR(300)),
    Column("retrieve_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("title", "publish_date")
)

oil_price_categories_table = Table(
    "oil_price_categories", meta,
    Column("category_id", INTEGER, primary_key=True, autoincrement=True),
    Column("category_name", VARCHAR(50), unique=True, nullable=False),
)

oil_price_indices_table = Table(
    "oil_price_indices", meta,
    Column("index_id", INTEGER, primary_key=True, autoincrement=True),
    Column("index_name", VARCHAR(50), unique=True, nullable=False),
    Column("category_id", INTEGER, ForeignKey("oil_price_categories.category_id"), nullable=True)
)

oil_price_table = Table(
    "oil_prices", meta,
    Column("id", INTEGER, primary_key=True, autoincrement=True),
    Column("index_id", INTEGER, ForeignKey("oil_price_indices.index_id"), nullable=False),
    Column("price", FLOAT, nullable=False),
    Column("price_time", DATETIME, nullable=False),
    Column("retrieve_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
)


def utest():
    meta.bind = test_engine

    item = {"title": "test1", "publish_date": "1998-7-2 22:00:00", "author": "sean", "content": 'testtet?',
            "random": "test"}
    use_item = {k: v for k, v in item.items() if k in oil_news_table.columns}
    query = oil_news_table.insert().values(use_item)
    print(query)


if __name__ == "__main__":
    utest()
