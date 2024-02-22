from orm import Engine
from orm.sql import POSTGRESQL_PARSER, String, Integer

connection_string = "postgresql://postgres:Qwerty22333@localhost:5432/postgres"
engine = Engine(connection_string)

class TableName:
    id = (Integer(), 'NOTNULL')
    username = String()
    email = int()

for _ in range(1):
    engine.create_table(TableName)
