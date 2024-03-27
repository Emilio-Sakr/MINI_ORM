import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from orm.sql import *
from orm import Engine
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Connecting to the DB
connection_string = "postgresql://postgres:Qwerty22333@localhost:5432/postgres"
engine = Engine(connection_string, logger=logger, min_pool_size=3)

# Designing the Tables
class Usernames(TableBase):
    matricule = (Integer(type='INT'), 'UNIQUE')
    username = String(type='VARCHAR', n=100)
    email = String(type='VARCHAR', n=200)
    password = (String('VARCHAR', n=100), 'CHECK ($ <> username AND CHAR_LENGTH($) >= 8)')

# Creating the tables
engine.create_table(Usernames)

# Connecting Tables to engine
Usernames.connect_to(engine)

command = 3

# Inserting Rows
if command == 0:
    Usernames.insert(matricule=12345, username='user1', email='user1@example.com', password='password123')
    data_to_insert = [
        {'matricule': 54321, 'username': 'user2', 'email': 'user2@example.com', 'password': 'password456'},
        {'matricule': 98765, 'username': 'user3', 'password': 'password789', 'email': 'user3@example.com'}
    ]
    Usernames.insert_all(data_to_insert)

# Deleting Rows
elif command == 1:
    Usernames.delete('*')  # Or simply Usernames.delete()
    Usernames.delete(filter_by='matricule = 12345')

# Updating Rows
elif command == 2:
    Usernames.update(filter_by='matricule = 54321', username='new_user', email='new_email@example.com')

# Selecting Data
elif command == 3:
    result = Usernames.select('*')
    print(result)

    result = Usernames.select(['username', 'email'])
    print(result)

    result = Usernames.select('*', filter_by='matricule = 54321')
    print(result)
