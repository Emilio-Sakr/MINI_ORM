from .url import url_parser
from .pool import ConnectionPool
from .connector import ConnectorHandler

class Engine:
    def __init__(self, url_string: str, **kwargs) -> None:
        self.URL = url_parser(url_string, **kwargs)
        self.pool = ConnectionPool(self.URL, **self.URL.pool)

    def create_table(self, table_name):
        handler = ConnectorHandler(self.pool)

        sql_create_table = """
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INT
            );
            """.format(table_name)
        handler.execute_query(sql_create_table)
        handler.close()