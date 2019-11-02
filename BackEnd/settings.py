from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

__sql_url = "mysql+pymysql://oil:h1VHhQWour@localhost:3306/"
__production_schema = 'oil_analysis'
__test_schema = 'oil_analysis_test'

# choose between production schema and test schema
schema = __production_schema

engine = create_engine(__sql_url + schema)

Base = declarative_base(bind=engine)
