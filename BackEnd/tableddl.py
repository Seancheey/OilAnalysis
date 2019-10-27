from BackEnd.objects import *
from sqlalchemy import Table

meta = Base.metadata

oil_news_table: Table = OilNews.__table__
oil_price_categories_table: Table = OilCategory.__table__
oil_price_indices_table: Table = OilIndex.__table__
oil_price_table: Table = OilPrice.__table__
oil_stock_categories_table: Table = OilStockCategory.__table__
oil_stocks_table: Table = OilStock.__table__
user_table: Table = User.__table__
login_table: Table = LoginSession.__table__
comment_table: Table = Comment.__table__
