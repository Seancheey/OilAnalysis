from sqlalchemy import MetaData
from sqlalchemy.sql import text
from sqlalchemy.schema import Table, Column, UniqueConstraint, ForeignKey
from sqlalchemy.types import VARCHAR, TEXT, INTEGER, TIMESTAMP, DATETIME, FLOAT
from BackEnd.settings import engine

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
    Column("retrieve_time", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
)

oil_stock_categories_table = Table(
    "oil_stock_categories", meta,
    Column("stock_id", INTEGER, primary_key=True, autoincrement=True),
    Column("stock_name", VARCHAR(50), nullable=False, unique=True),
)

oil_stocks_table = Table(
    "oil_stocks", meta,
    Column("id", INTEGER, primary_key=True, autoincrement=True),
    Column("stock_id", INTEGER, ForeignKey("oil_stock_categories.stock_id"), nullable=False),
    Column("volume", FLOAT, nullable=False),
    Column("update_time", DATETIME, nullable=False, ),
    Column("retrieve_time", TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    UniqueConstraint("update_time", "stock_id")
)

user_table = Table(
    "users", meta,
    Column("username", VARCHAR(32), primary_key=True),
    Column("email", VARCHAR(64), unique=True, nullable=False),
    Column("pass", VARCHAR(256), nullable=False)
)

login_table = Table(
    "login_sessions", meta,
    Column("session_token", VARCHAR(32), primary_key=True),
    Column("username", VARCHAR(32), ForeignKey("users.username"), nullable=False),
    Column("expiration_time", TIMESTAMP, nullable=False)
)

comment_table = Table(
    "comments", meta,
    Column("comment_id", primary_key=True, autoincrement=True),
    Column("news_id", INTEGER, ForeignKey("oil_news.id"), nullable=False),
    Column("username", VARCHAR(32), ForeignKey("users.username"), nullable=False),
    Column("text", TEXT, nullable=False)
)
