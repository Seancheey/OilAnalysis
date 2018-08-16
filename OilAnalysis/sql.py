from sqlalchemy import create_engine
import sqlalchemy.engine

local_engine = create_engine("mysql+pymysql://root@localhost:3306/oil_analysis")

__type_map = {int: "int", float: "float", str: "text"}


def insert_values(engine_or_connection, table_name: str, entries):
	if type(entries) == dict:
		engine_or_connection.execute(__gen_insert_query(table_name, entries))
	elif type(entries) == list:
		for entry in entries:
			engine_or_connection.execute(__gen_insert_query(table_name, entry))
	else:
		raise TypeError("entries with type %s is not supported" % type(entries))


def has_table(engine_or_connection: sqlalchemy.engine.Engine, table_name: str, schema=None) -> bool:
	return engine_or_connection.has_table(table_name, schema=schema)


def create_table(engine: sqlalchemy.engine.Engine, table_name: str, sample_entry: dict, suffix: dict = None):
	table_columns = []
	types = __get_sql_types(sample_entry)
	for col, val in sample_entry.items():
		suf = suffix[col] if col in suffix else ""
		table_columns.append("%s %s %s" % (col, types[col], suf))
	engine.execute("CREATE TABLE IF NOT EXISTS %s(%s)" % (table_name, ",".join(table_columns)))


def __gen_insert_query(table_name: str, values: dict):
	columns = ",".join(values.keys())
	col_values = ",".join([str(value) if type(value) != str else "'%s'" % value for value in values.values()])
	return "INSERT INTO %s(%s) VALUES (%s);" % (table_name, columns, col_values)


def __get_sql_types(sample_entry) -> dict:
	out = {}
	for col, val in sample_entry.items():
		if type(val) in __type_map.keys():
			out[col] = __type_map[type(val)]
		else:
			raise TypeError("type if column %s: %s does not match any mappable sql types" % col, type(val))
	return out


def __unit_test():
	create_table(local_engine, "sql_test", {"id": 123, "title": "iraq", "excerpt": "yoobuddy"}, {"id": "primary key"})
	insert_values(local_engine, "sql_test", {"id": 123, "title": "iraq", "excerpt": "yoobuddy"})


if __name__ == "__main__":
	__unit_test()
