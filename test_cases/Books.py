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
class Genres(TableBase):
    id = (Integer(type='SMALLINT'), 'UNIQUE')
    name = String(type='VARCHAR', n=100)

class Books(TableBase):
    id = (Integer(type='SERIAL'), 'PRIMARY KEY')
    title = String(type='VARCHAR', n=255)
    author = String(type='VARCHAR', n=255)
    published_year = Integer()
    genre_id = Integer()
    genre = ForeignKey('genres(id)', 'genre_id')
    unique_title_author = Index('title', 'author', unique=True)

# Creating the tables
engine.create_table(Genres)
engine.create_table(Books)

# Connecting Tables to engine
Books.connect_to(engine)
Genres.connect_to(engine)

command = 1
# Inserting data into tables
if command == 0:
    Genres.insert(name='Historical Fiction', id = 1)
    Genres.insert(name='Thriller', id = 2)
    Genres.insert(name='Horror', id = 3)
    Genres.insert(name='Biography', id = 4)
    Genres.insert(name='Self-Help', id = 5)
    Genres.insert(name='Fantasy', id = 6)
    Genres.insert(name='Dystopian', id = 7)

    Books.insert(title='To Kill a Mockingbird', author='Harper Lee', published_year=1960, genre_id=1)
    Books.insert(title='The Catcher in the Rye', author='J.D. Salinger', published_year=1951, genre_id=2)
    Books.insert(title='The Lord of the Rings', author='J.R.R. Tolkien', published_year=1954, genre_id=6) 
    Books.insert(title='Gone with the Wind', author='Margaret Mitchell', published_year=1936, genre_id=1)
    Books.insert(title='The Girl with the Dragon Tattoo', author='Stieg Larsson', published_year=2005, genre_id=2)
    Books.insert(title='Pride and Prejudice', author='Jane Austen', published_year=1813, genre_id=1)
    Books.insert(title='Harry Potter and the Philosopher''s Stone', author='J.K. Rowling', published_year=1997, genre_id=6)
    Books.insert(title='The Hobbit', author='J.R.R. Tolkien', published_year=1937, genre_id=6)
    Books.insert(title='1984', author='George Orwell', published_year=1949, genre_id=7)
    Books.insert(title='The Da Vinci Code', author='Dan Brown', published_year=2003, genre_id=2)


# Query for data
elif command==1:
    print(Books.select('*', filter_by=('genre_id = 2', 'published_year = 1951')))

# Delete all element from table
elif command==2:
    Books.delete('*') # or Books.delete() 
    Genres.delete('*')