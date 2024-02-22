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
        