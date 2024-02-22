from orm.sql import POSTGRESQL_PARSER, String, Integer

class User:
    username = (String(), 'NOT NULL')
    email = String()

POSTGRESQL_PARSER.create_table(User)