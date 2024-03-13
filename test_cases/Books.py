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
    available = Boolean()
    author = String(type='VARCHAR', n=255)
    published_year = (Integer(), 'NOT NULL')
    genre_id = Integer()
    genre = (ForeignKey('genres(id)', 'genre_id'), 'ON DELETE CASCADE')
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
    Books.delete('*') # or Books.delete() 
    Genres.delete('*')
    Genres.insert(name='Historical Fiction', id = 1)
    Genres.insert(name='Thriller', id = 2)
    Genres.insert(name='Horror', id = 3)
    Genres.insert(name='Biography', id = 4)
    Genres.insert(name='Self-Help', id = 5)
    Genres.insert(name='Fantasy', id = 6)
    Genres.insert(name='Dystopian', id = 7)
    Genres.insert(name='Mystery', id = 8)
    Genres.insert(name='Romance', id = 9)

    Books.insert(title='To Kill a Mockingbird', author='Harper Lee', published_year=1960, genre_id=1, available = True)
    Books.insert(title='The Catcher in the Rye', author='J.D. Salinger', published_year=1951, genre_id=2, available = True)
    Books.insert(title='The Lord of the Rings', author='J.R.R. Tolkien', published_year=1954, genre_id=6, available = True) 
    Books.insert(title='Gone with the Wind', author='Margaret Mitchell', published_year=1936, genre_id=1, available = True)
    Books.insert(title='The Girl with the Dragon Tattoo', author='Stieg Larsson', published_year=2005, genre_id=2, available = True)
    Books.insert(title='Pride and Prejudice', author='Jane Austen', published_year=1813, genre_id=1, available = True)
    Books.insert(title='Harry Potter and the Philosopher''s Stone', author='J.K. Rowling', published_year=1997, genre_id=6, available = True)
    Books.insert(title='The Hobbit', author='J.R.R. Tolkien', published_year=1937, genre_id=6, available = True)
    Books.insert(title='1984', author='George Orwell', published_year=1949, genre_id=7, available = True)
    Books.insert(title='The Da Vinci Code', author='Dan Brown', published_year=2003, genre_id=2, available = True)
    Books.insert(title='A good girl guide''s to murder', author='Holly Jackson', published_year=2019, genre_id=8, available = True)
    Books.insert(title='Twisted Love', author='Ana Huang', published_year=2021,available = True,  genre_id=9)

elif command==1:
    Books.delete('*') # or Books.delete() 
    Genres.delete('*')
    genres_data = [
        {'name': 'Historical Fiction', 'id': 1},
        {'name': 'Thriller', 'id': 2},
        {'name': 'Horror', 'id': 3},
        {'name': 'Biography', 'id': 4},
        {'name': 'Self-Help', 'id': 5},
        {'name': 'Fantasy', 'id': 6},
        {'name': 'Dystopian', 'id': 7},
        {'name': 'Mystery', 'id': 8},
        {'name': 'Romance', 'id': 9}
    ]
    books_data = [
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'published_year': 1960, 'genre_id': 1, 'available': True},
        {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'published_year': 1951, 'genre_id': 2, 'available': True},
        {'title': 'The Lord of the Rings', 'author': 'J.R.R. Tolkien', 'published_year': 1954, 'genre_id': 6, 'available': True},
        {'title': 'Gone with the Wind', 'author': 'Margaret Mitchell', 'published_year': 1936, 'genre_id': 1, 'available': True},
        {'title': 'The Girl with the Dragon Tattoo', 'author': 'Stieg Larsson', 'published_year': 2005, 'genre_id': 2, 'available': True},
        {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'published_year': 1813, 'genre_id': 1, 'available': True},
        {'title': 'Harry Potter and the Philosopher''s Stone', 'author': 'J.K. Rowling', 'published_year': 1997, 'genre_id': 6, 'available': True},
        {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'published_year': 1937, 'genre_id': 6, 'available': True},
        {'title': '1984', 'author': 'George Orwell', 'published_year': 1949, 'genre_id': 7, 'available': True},
        {'title': 'The Da Vinci Code', 'author': 'Dan Brown', 'published_year': 2003, 'genre_id': 2, 'available': True},
        {'title': 'A good girl guide''s to murder', 'author': 'Holly Jackson', 'published_year': 2019, 'genre_id': 8, 'available': True},
        {'title': 'Twisted Love', 'author': 'Ana Huang', 'published_year': 2021, 'available': True, 'genre_id': 9}
    ]
    Genres.insert_all(genres_data)
    Books.insert_all(books_data)

# Query for data
elif command==2:
    print(Books.select('*'))
    print(Books.select(limit=2, offset=4))
    print(Books.select(filter_by={'author': 'Ja%'}, order_by='published_year ASC', limit=2))
    print(Books.select('author published_year title', filter_by={'author': 'Ja%'}, order_by='published_year ASC', limit=2))
    print(Books.select('*', filter_by=('genre_id = 2', 'published_year = 2003')))


# Delete all element from table
elif command==3:
    Books.delete('*') # or Books.delete() 
    Genres.delete('*')