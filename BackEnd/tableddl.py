from BackEnd.objects import *
from sqlalchemy import Table

meta = Base.metadata

oil_news_table: Table = OilNews.__table__
oil_price_categories_table: Table = OilCategory.__table__
oil_price_indices_table: Table = OilIndex.__table__
oil_price_table: Table = OilPrice.__table__
user_table: Table = User.__table__
login_table: Table = LoginSession.__table__
news_comments_table = NewsComment.__table__
price_comments_table = PriceComment.__table__
