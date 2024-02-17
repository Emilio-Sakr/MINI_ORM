#import sqlite3
#import pymysql
import psycopg2

class DBConnector:
    def __init__(self, server, host, user, password, database):
        self.db_type = server
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    def connect(self):
        if self.db_type == 'postgresql':
            self.connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        else:
            raise ValueError("Unsupported database type")
        
        self.cursor = self.connection.cursor()
    
    def execute_query(self, query):
        if not self.connection:
            self.connect()
        
        self.cursor.execute(query)
        self.connection.commit()
        if self.cursor.description is not None:
            return self.cursor.fetchall()
        else:
            return None
    
    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.connection.close()