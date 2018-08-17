oil_news_table_name = "oil_news"
col_id = "id"
col_title = "title"
col_date = "publish_date"
col_author = "author"
col_content = "content"
col_timestamp = "create_time"

oil_news_column_types = {
	col_id: "int",
	col_title: "VARCHAR(100)",
	col_date: "date",
	col_author: "VARCHAR(100)",
	col_content: "text",
	col_timestamp: "TIMESTAMP"
}

oil_news_column_suffix = {
	col_id: "primary key AUTO_INCREMENT",
	col_title: "not null",
	col_date: "not null",
	col_author: "not null",
	col_content: "not null",
	col_timestamp: "default CURRENT_TIMESTAMP"
}
