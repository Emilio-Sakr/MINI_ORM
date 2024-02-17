from lib import Engine

connection_string = "postgresql://postgres:Qwerty22333@localhost:5432/postgres"
engine = Engine(connection_string)

for _ in range(1):
    engine.create_table('settak_table')
