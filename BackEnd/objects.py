from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from sqlalchemy.schema import Column, UniqueConstraint, ForeignKey
from sqlalchemy.types import VARCHAR, TEXT, INTEGER, TIMESTAMP, DATETIME, FLOAT, VARBINARY, CHAR
from BackEnd.settings import engine

Base = declarative_base(bind=engine)


class OilNews(Base):
    __tablename__ = "oil_news"
    __table_args__ = (UniqueConstraint("title", "publish_date"),)
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(100), nullable=False)
    publish_date = Column(DATETIME, nullable=False)
    author = Column(VARCHAR(100))
    content = Column(TEXT, nullable=False)
    reference = Column(VARCHAR(300))
    retrieve_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    def __repr__(self):
        return "OilNews(id=%d, title=%s)" % (self.id, self.title)


class OilCategory(Base):
    __tablename__ = "oil_price_categories"
    category_id = Column(INTEGER, primary_key=True, autoincrement=True)
    category_name = Column(VARCHAR(50), unique=True, nullable=False)


class OilIndex(Base):
    __tablename__ = "oil_price_indices"
    index_id = Column(INTEGER, primary_key=True, autoincrement=True)
    index_name = Column(VARCHAR(50), unique=True, nullable=False)
    category_id = Column(INTEGER, ForeignKey("oil_price_categories.category_id"), nullable=True)


class OilPrice(Base):
    __tablename__ = "oil_prices"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    index_id = Column(INTEGER, ForeignKey("oil_price_indices.index_id"), nullable=False)
    price = Column(FLOAT, nullable=False)
    price_time = Column(DATETIME, nullable=False)
    retrieve_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class OilStockCategory(Base):
    __tablename__ = "oil_stock_categories"
    stock_id = Column(INTEGER, primary_key=True, autoincrement=True)
    stock_name = Column(VARCHAR(50), nullable=False, unique=True)


class OilStock(Base):
    __tablename__ = "oil_stocks"
    __tableargs__ = (UniqueConstraint("update_time", "stock_id"),)
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    stock_id = Column(INTEGER, ForeignKey("oil_stock_categories.stock_id"), nullable=False)
    volume = Column(FLOAT, nullable=False)
    update_time = Column(DATETIME, nullable=False, )
    retrieve_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))


class User(Base):
    __tablename__ = "users"
    username = Column(VARCHAR(32), primary_key=True)
    email = Column(VARCHAR(64), unique=True, nullable=False)
    password = Column(VARBINARY(32), nullable=False)


class LoginSession(Base):
    __tablename__ = "login_sessions"
    session_token = Column(CHAR(16), primary_key=True)
    username = Column(VARCHAR(32), ForeignKey("users.username"), nullable=False)
    expiration_time = Column(TIMESTAMP, nullable=False)


class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(INTEGER, primary_key=True, autoincrement=True)
    news_id = Column(INTEGER, ForeignKey("oil_news.id"), nullable=False)
    username = Column(VARCHAR(32), ForeignKey("users.username"), nullable=False)
    text = Column(TEXT, nullable=False)
