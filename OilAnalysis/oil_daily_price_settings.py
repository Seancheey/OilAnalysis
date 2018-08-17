col_id = "id"
col_category = "category"
col_index_name = "index_name"
col_last = "last_price"
col_abs_change = "abs_change"
col_per_change = "per_change"
col_update_time = "update_time"

oil_daily_price_column_types = {
	col_id: "int",
	col_category: "VARCHAR(40)",
	col_index_name: "VARCHAR(50)",
	col_last: "float",
	col_abs_change: "float",
	col_per_change: "float",
	col_update_time: "TIMESTAMP"
}

oil_daily_price_column_suffix = {
	col_id: "primary key",
	col_index_name: "not null",
	col_last: "not null",
	col_category: "null",
	col_abs_change: "null",
	col_per_change: "null",
	col_update_time: "not null default CURRENT_TIMESTAMP"
}
