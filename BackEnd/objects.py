from sqlalchemy.sql import text
from sqlalchemy.schema import Column, UniqueConstraint, ForeignKey
from sqlalchemy.types import VARCHAR, TEXT, INTEGER, TIMESTAMP, DATETIME, FLOAT, VARBINARY, CHAR
from sqlalchemy.ext.declarative import declared_attr
from BackEnd.settings import Base


class OilNews(Base):
    __tablename__ = "oil_news"
    __table_args__ = (UniqueConstraint("title", "publish_date"),)
    news_id = Column(INTEGER, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(100), nullable=False)
    publish_date = Column(DATETIME, nullable=False)
    author = Column(VARCHAR(100))
    content = Column(TEXT, nullable=False)
    reference = Column(VARCHAR(300))
    retrieve_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    def __repr__(self):
        return "OilNews(id=%d, title=%s)" % (self.news_id, self.title)


class OilCategory(Base):
    __tablename__ = "oil_price_categories"
    category_id = Column(INTEGER, primary_key=True, autoincrement=True)
    category_name = Column(VARCHAR(50), unique=True, nullable=False)


class OilIndex(Base):
    __tablename__ = "oil_price_indices"
    index_id = Column(INTEGER, primary_key=True, autoincrement=True)
    index_name = Column(VARCHAR(50), unique=True, nullable=False)
    category_id = Column(INTEGER, ForeignKey("oil_price_categories.category_id", ondelete='CASCADE'), nullable=True)


class OilPrice(Base):
    __tablename__ = "oil_prices"
    price_id = Column(INTEGER, primary_key=True, autoincrement=True)
    index_id = Column(INTEGER, ForeignKey("oil_price_indices.index_id", ondelete='CASCADE'), nullable=False)
    price = Column(FLOAT, nullable=False)
    price_time = Column(DATETIME, nullable=False)
    retrieve_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class User(Base):
    __tablename__ = "users"
    username = Column(VARCHAR(32), primary_key=True)
    email = Column(VARCHAR(64), unique=True, nullable=False)
    password = Column(VARBINARY(32), nullable=False)


class LoginSession(Base):
    __tablename__ = "login_sessions"
    session_token = Column(CHAR(16), primary_key=True)
    username = Column(VARCHAR(32), ForeignKey("users.username", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    login_time = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    expiration_time = Column(TIMESTAMP, nullable=True)
    device_name = Column(VARCHAR(64), nullable=True)


class Comment(object):
    """
    ISA Parent of new, price, followup comments table
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def comment_id(cls):
        return Column(INTEGER, primary_key=True, autoincrement=True)

    @declared_attr
    def username(cls):
        return Column(VARCHAR(32), ForeignKey("users.username", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    @declared_attr
    def comment_time(cls):
        return Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    @declared_attr
    def text(cls):
        return Column(TEXT, nullable=False)


class NewsComment(Comment, Base):
    __tablename__ = "news_comments"
    target_id = Column(INTEGER, ForeignKey("oil_news.news_id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    reply_id = Column(INTEGER, ForeignKey("news_comments.comment_id", ondelete='CASCADE', onupdate='CASCADE'),
                      nullable=True)


class PriceComment(Comment, Base):
    __tablename__ = "price_comments"
    target_id = Column(INTEGER, ForeignKey("oil_price_indices.index_id", ondelete='CASCADE', onupdate='CASCADE'),
                       nullable=False)
    reply_id = Column(INTEGER, ForeignKey("price_comments.comment_id", ondelete='CASCADE', onupdate='CASCADE'),
                      nullable=True)
