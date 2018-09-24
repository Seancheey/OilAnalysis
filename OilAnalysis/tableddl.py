from sqlalchemy import MetaData
from sqlalchemy.sql import text
from sqlalchemy.schema import Table, Column, UniqueConstraint, ForeignKey
from sqlalchemy.types import VARCHAR, TEXT, INTEGER, TIMESTAMP, DATETIME, FLOAT
from OilAnalysis.settings import test_engine, engine

meta = MetaData()
meta.bind = engine

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
