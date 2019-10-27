from sqlalchemy import create_engine

__local_engine = create_engine("mysql+pymysql://sean:371sqySQY@localhost:3306/oil_analysis")
test_engine = create_engine("mysql+pymysql://sean:371sqySQY@localhost:3306/test")

engine = test_engine
