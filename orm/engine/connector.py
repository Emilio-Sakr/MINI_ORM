from .pool import ConnectionPool

class ConnectorHandler:
    def __init__(self, resource: ConnectionPool):
        self.resource = resource
        self.connection = self.resource.acquire()
        self.cursor = self.connection.cursor()
    
    def execute_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        if self.cursor.description is not None:
            return self.cursor.fetchall()
        else:
            return None
    
    def close(self):
        if self.connection:
            self.cursor.close()
            self.resource.release(self.connection)