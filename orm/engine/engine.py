from .url import url_parser
from .pool import ConnectionPool
from .connector import ConnectorHandler
from ..sql import POSTGRESQL_PARSER

class Engine:
    def __init__(self, url_string: str, **kwargs) -> None:
        self.URL = url_parser(url_string, **kwargs)
        self.pool = ConnectionPool(self.URL, **self.URL.pool)
        self.postgresql = 'postgresql'

    def create_table(self, table: object):
        handler = ConnectorHandler(self.pool)

        if self.URL.server == self.postgresql:
            sql_create_table = POSTGRESQL_PARSER.create_table(table)
            print(sql_create_table)

        handler.execute_query(sql_create_table)
        handler.close()
        
    def insert(self, table, **kwargs):
        handler = ConnectorHandler(self.pool)

        if self.URL.server == self.postgresql:
            sql_insert_into_table = POSTGRESQL_PARSER.insert(table, **kwargs)
            print(sql_insert_into_table)

        handler.execute_query(sql_insert_into_table)
        handler.close()

    def update(self, table, filter_clause, **kwargs):
        handler = ConnectorHandler(self.pool)

        if self.URL.server == self.postgresql:
            sql_update_table = POSTGRESQL_PARSER.update(table, filter_clause, **kwargs)
            print(sql_update_table)

        handler.execute_query(sql_update_table)
        handler.close()

    def delete(self, table, filter_clause):
        handler = ConnectorHandler(self.pool)

        if self.URL.server == self.postgresql:
            sql_delete_from_table = POSTGRESQL_PARSER.delete(table, filter_clause)
            print(sql_delete_from_table)

        handler.execute_query(sql_delete_from_table)
        handler.close()

    def select(self, table, columns, filter_by, order_by, limit):
        handler = ConnectorHandler(self.pool)

        if self.URL.server == self.postgresql:
            sql_select_from_table = POSTGRESQL_PARSER.select(table, columns, filter_by, order_by, limit)
            print(sql_select_from_table)

        data = handler.execute_query(sql_select_from_table)
        handler.close()
        return data