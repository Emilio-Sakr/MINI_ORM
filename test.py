from orm import Engine
from orm.sql import POSTGRESQL_PARSER, String, Integer, TableBase

connection_string = "postgresql://postgres:Qwerty22333@localhost:5432/postgres"
engine = Engine(connection_string, min_pool_size=3)

class TableName(TableBase):
    id = Integer(type='SMALLINT')
    username = (String(type='VARCHAR', n=10), 'CHECK (LENGTH($) <= 10)')
    email = Integer()

for _ in range(1):
    #engine.create_table(TableName)
    TableName.connect_to(engine)
    #TableName.insert(id = 1, username='emilio', email=2)
    #TableName.update('id = 1', username='Emilio', email=3)
    TableName.delete('id = 1')
    #engine.update_table('tablename', {'username: Rodol'})