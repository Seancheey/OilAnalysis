from datetime import datetime


class TableDDL:
    __slots__ = "table_name", "column_definitions", "constraints"

    def __init__(self, table_name, column_definitions, constraints=None):
        self.table_name = table_name
        self.column_definitions = column_definitions
        self.constraints = constraints

    @property
    def column_types(self):
        return {col_name: (definition[0] if type(definition) == tuple else definition) for col_name, definition in
                self.column_definitions.items()}

    @property
    def column_suffix(self):
        return {col_name: (definition[1] if type(definition) == tuple else "") for col_name, definition in
                self.column_definitions.items()}

    @property
    def create_query(self):
        entries = ["%s %s %s" % (c, t, self.column_suffix[c] if c in self.column_suffix else "") for c, t in
                   self.column_types.items()]
        return "CREATE TABLE IF NOT EXISTS %s(%s, %s)" % (self.table_name, ",".join(entries), self.constraints)

    def insert_query(self, values: dict):
        for col_name in values.keys():
            if col_name not in self.column_definitions:
                raise KeyError("column name: %s is not found in DDL of %s" % (col_name, self.table_name))
        columns = ",".join(values.keys())
        col_values = ",".join(
            [str(value) if type(value) not in [datetime, str] else "'%s'" % value for value in values.values()]
        )
        return "INSERT INTO %s(%s) VALUES (%s);" % (self.table_name, columns, col_values)


oil_news_DDL = TableDDL(
    table_name="oil_news",
    column_definitions={
        "id": ("int", "primary key AUTO_INCREMENT"),
        "title": ("VARCHAR(100)", "not null"),
        "publish_date": ("date", "not null"),
        "author": ("VARCHAR(100)", "not null"),
        "content": ("text", "not null"),
        "create_time": ("TIMESTAMP", "default CURRENT_TIMESTAMP"),
    }
)
oil_price_categories_DDL = TableDDL(
    table_name="oil_price_categories",
    column_definitions={
        "category_id": ("int", "auto_increment primary key"),
        "category_name": ("varchar(50)", "not null")
    },
    constraints="constraint oil_price_categories_category_name_uindex\
  unique (category_name)"
)

oil_price_indices_DDL = TableDDL(
    table_name="oil_price_indices",
    column_definitions={
        "index_id": ("int", "auto_increment primary key"),
        "index_name": ("varchar(50)", "null"),
        "category_id": ("int", "null")
    },
    constraints="constraint category_fk foreign key (category_id) references oil_price_categories (category_id)"
)

oil_price_DDL = TableDDL(
    table_name="oil_prices",
    column_definitions={
        "id": ("int", "auto_increment primary key"),
        "index_id": ("int", "not null"),
        "price": ("float", "not null"),
        "price_time": ("datetime", "not null"),
        "retrieve_time": ("timestamp", "default CURRENT_TIMESTAMP")
    },
    constraints="constraint oil_prices_oil_price_indices_index_id_fk\
  foreign key (index_id) references oil_price_indices (index_id)"
)


def utest():
    print(oil_price_DDL.create_query)


if __name__ == "__main__":
    utest()
