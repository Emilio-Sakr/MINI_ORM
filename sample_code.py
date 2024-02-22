from orm.sql import POSTGRESQL_PARSER, String, Integer

class User:
    matricule = (String(type='VARCHAR', n=10), 'PRIMARY KEY')
    username = String(),
    email = String()

print(POSTGRESQL_PARSER.create_table(User))