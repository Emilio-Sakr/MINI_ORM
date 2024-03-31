from psycopg2 import pool

from .url import URL
from ..exc import ConstructionError, ResourceError        

class ConnectionPool:
    '''
    This will create a connection pool from which we will take connectors to access the database
    '''
    def __init__(self, URL: URL, min_pool_size: int = 1, max_pool_size: int = 5):
        self.max_pool_size = int(max_pool_size)
        self.min_pool_size = int(min_pool_size)
        if self.max_pool_size<self.min_pool_size:
            self.max_pool_size = self.min_pool_size
        self.URL = URL

        self.postgresql = 'postgresql'

        self._create_pool()
        
    def _create_pool(self) -> None:
        if self.URL.server == self.postgresql:
            postgreSQL_pool = pool.SimpleConnectionPool(
                self.min_pool_size, 
                self.max_pool_size,
                user=self.URL.username,
                password=self.URL.password,
                host=self.URL.host,
                port=self.URL.port,
                database=self.URL.database)
            
            if not (postgreSQL_pool):
                raise ConstructionError('Error in constructing connection pool')
            
            self.pool = postgreSQL_pool
        else:
            raise ConstructionError('Server does not support pool construction')

    def acquire(self):
        if self.URL.server == self.postgresql:
            connection = self.pool.getconn()
            if connection: return connection
            else: raise ResourceError('cannot retrieve connection from pool')

    def release(self, connection):
        if self.URL.server == self.postgresql:
            self.pool.putconn(connection)

    def close_all(self):
        if self.URL.server == self.postgresql:
            self.pool.closeall()