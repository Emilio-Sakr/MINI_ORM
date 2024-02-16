#import sqlite3
#import pymysql
import psycopg2

class DBConnector:
    def __init__(self, db_type, host, user, password, database):
        self.db_type = db_type
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    def connect(self):
        #if self.db_type == 'sqlite':
        #    self.connection = sqlite3.connect(self.database)
        #elif self.db_type == 'mysql':
        #    self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        if self.db_type == 'postgresql':
            self.connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        else:
            raise ValueError("Unsupported database type")
        
        self.cursor = self.connection.cursor()
    
    def execute_query(self, query):
        if not self.connection:
            self.connect()
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

#connector_sqlite = DBConnector(db_type='sqlite', host=None, user=None, password=None, database='example.db')
#connector_mysql = DBConnector(db_type='mysql', host='localhost', user='root', password='password', database='example')
connector_postgresql = DBConnector(db_type='postgresql', host='localhost', user='postgres', password='password', database='example')

#connector_sqlite.connect()
#connector_mysql.connect()
connector_postgresql.connect()

#sqlite_result = connector_sqlite.execute_query("SELECT * FROM my_table")
#mysql_result = connector_mysql.execute_query("SELECT * FROM my_table")
postgresql_result = connector_postgresql.execute_query("SELECT * FROM my_table")

#connector_sqlite.close()
#connector_mysql.close()
connector_postgresql.close()
