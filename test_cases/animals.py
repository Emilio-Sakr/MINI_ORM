import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from orm.sql import *
from orm import Engine

# Connecting to the DB
connection_string = "postgresql://postgres:Qwerty22333@localhost:5432/postgres"
engine = Engine(connection_string, min_pool_size=3)

# Designing the Tables
class Animals(TableBase):
    id = (Integer(type='SERIAL'), 'PRIMARY KEY')
    name = String(type='VARCHAR', n=255)
    age = Integer()

class Birds(Animals):
    color = String(type='VARCHAR', n=100) 

class Cats(Animals):
    breed = String(type='VARCHAR', n=100) 

class Dogs(Animals):
    breed = String(type='VARCHAR', n=100) 
    size = String(type='VARCHAR', n=50) 

# Creating the tables
engine.create_table_inherit(Birds)
engine.create_table_inherit(Cats)
engine.create_table_inherit(Dogs)

# Connecting Tables to engine
Birds.connect_to(engine)
Cats.connect_to(engine)
Dogs.connect_to(engine)

command = 2

# Inserting data into tables
if command == 0:
    Birds.delete('*')
    Cats.delete('*')
    Dogs.delete('*')

    Birds.insert(name='Parrot', age=5, color='Green')
    Cats.insert(name='Siamese', age=3, breed='Siamese')
    Dogs.insert(name='Labrador', age=2, breed='Labrador', size='Large')

elif command==1:
    Birds.delete('*')
    Cats.delete('*')
    Dogs.delete('*')

    birds_data = [
        {'name': 'Parrot', 'age': 5, 'color': 'Green'},
        {'name': 'Eagle', 'age': 7, 'color': 'Brown'},
        {'name': 'Owl', 'age': 3, 'color': 'Gray'},
    ]
    cats_data = [
        {'name': 'Siamese', 'age': 3, 'breed': 'Siamese'},
        {'name': 'Persian', 'age': 4, 'breed': 'Persian'},
        {'name': 'Maine Coon', 'age': 2, 'breed': 'Maine Coon'},
    ]
    dogs_data = [
        {'name': 'Labrador', 'age': 2, 'breed': 'Labrador', 'size': 'Large'},
        {'name': 'German Shepherd', 'age': 3, 'breed': 'German Shepherd', 'size': 'Large'},
        {'name': 'Golden Retriever', 'age': 1, 'breed': 'Golden Retriever', 'size': 'Large'},
    ]
    Birds.insert_all(birds_data)
    Cats.insert_all(cats_data)
    Dogs.insert_all(dogs_data)

elif command == 2:
    print("Birds:")
    print(Birds.select('*'))

    print("\nCats:")
    print(Cats.select())

    print("\nDogs:")
    print(Dogs.select())

    print("\nBirds (Name and Color):")
    print(Birds.select('name color'))
    # or
    #print(Birds.select(('name', 'color')))
    #print(Birds.select(['name', 'color']))

    print("\nDogs with age greater than 2:")
    print(Dogs.select('*', filter_by='age > 2'))
    # or
    #print(Dogs.select('*', filter_by=['age > 2']))
    #print(Dogs.select('*', filter_by=('age > 2')))
