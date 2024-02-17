import psycopg2
from queue import Queue
from threading import Lock, Semaphore
import logging
from typing import Optional

from ..engine import URL, DBConnector

class ConnectionPool:
    def __init__(self, URL: URL, pool_size: Optional[int] = 10, max_overflow: Optional[int] = 2, pool_timeout: Optional[int] = 10):
        self.pool_size = int(pool_size)
        self.max_overflow = int(max_overflow)
        self.pool_timeout = int(pool_timeout)
        self.URL = URL

        self.resources = Queue(maxsize=pool_size)
        self.lock = Lock()
        self.semaphore = Semaphore(pool_size)

        logging.info('Creating the connectors pool')
        for _ in range(pool_size):
            self._create_connection()
        logging.info('Finished creating the connectors pool')
        
        
    def _create_connection(self):
        try:
            db_connector = DBConnector(
                server='postgresql',
                host=self.URL.host,
                user=self.URL.username,
                password=self.URL.password,
                database=self.URL.database
            )
            db_connector.connect()
            self.resources.put(db_connector)
        except Exception as e:
            logging.error(f"Error creating connection: {e}")

    def acquire(self) -> ( None | DBConnector ):
        self.semaphore.acquire()
        try:
            connection = self.resources.get(timeout=self.pool_timeout)
            return connection
        except Exception as e:
            logging.error(f"Error acquiring connection: {e}", exc_info=True)
            return None

    def release(self, connection: DBConnector):
        try:
            self.resources.put(connection)
        except Exception as e:
            logging.error(f"Error releasing connection: {e}")
        finally:
            self.semaphore.release()

    def close_all(self):
        while not self.resources.empty():
            connection, db_connector = self.resources.get()
            db_connector.close()

    def expand_pool(self, additional_connections):
        with self.lock:
            for _ in range(additional_connections):
                self._create_connection()
            self.pool_size += additional_connections

    def shrink_pool(self, connections_to_remove):
        with self.lock:
            for _ in range(connections_to_remove):
                connection, db_connector = self.resources.get()
                db_connector.close()
            self.pool_size -= connections_to_remove