from OilAnalysis.sql import gen_insert_query, gen_create_query


class SQLSettings:
	__slots__ = "table_name", "column_types", "column_suffix"

	def __init__(self, table_name, column_types, column_suffix=None):
		self.table_name = table_name
		self.column_types = column_types
		self.column_suffix = column_suffix if column_suffix else {}

	def gen_create_query(self):
		return gen_create_query(self.table_name, self.column_types, self.column_suffix)

	def insert_query(self, values):
		return gen_insert_query(self.table_name, values)


col_news_id = "id"
col_news_title = "title"
col_news_date = "publish_date"
col_news_author = "author"
col_news_content = "content"
col_news_timestamp = "create_time"

oil_news_settings = SQLSettings(
	table_name="oil_news",
	column_types={
		col_news_id: "int",
		col_news_title: "VARCHAR(100)",
		col_news_date: "date",
		col_news_author: "VARCHAR(100)",
		col_news_content: "text",
		col_news_timestamp: "TIMESTAMP"
	},
	column_suffix={
		col_news_id: "primary key AUTO_INCREMENT",
		col_news_title: "not null",
		col_news_date: "not null",
		col_news_author: "not null",
		col_news_content: "not null",
		col_news_timestamp: "default CURRENT_TIMESTAMP"
	}
)

col_price_id = "id"
col_price_category = "category"
col_price_index_name = "index_name"
col_price_last = "last_price"
col_price_abs_change = "abs_change"
col_price_per_change = "per_change"
col_price_update_time = "update_time"
oil_daily_price_settings = SQLSettings(
	table_name="oil_daily_price",
	column_types={
		col_price_id: "int",
		col_price_category: "VARCHAR(40)",
		col_price_index_name: "VARCHAR(50)",
		col_price_last: "float",
		col_price_abs_change: "float",
		col_price_per_change: "float",
		col_price_update_time: "TIMESTAMP"
	},
	column_suffix={
		col_price_id: "primary key AUTO_INCREMENT",
		col_price_index_name: "not null",
		col_price_last: "not null",
		col_price_category: "null",
		col_price_abs_change: "null",
		col_price_per_change: "null",
		col_price_update_time: "not null default CURRENT_TIMESTAMP"
	}
)
