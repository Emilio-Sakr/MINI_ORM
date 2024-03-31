import os
import sys
import timeit
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from orm.sql import *
from orm import Engine

# Function to create engine and measure time
def create_engine(connection_string):
    start_time = timeit.default_timer()
    engine = Engine(connection_string, min_pool_size=3)
    elapsed_time = timeit.default_timer() - start_time
    return engine, elapsed_time

# Function to create table and measure time
def create_table(engine, table_class):
    start_time = timeit.default_timer()
    engine.create_table(table_class)
    elapsed_time = timeit.default_timer() - start_time
    return elapsed_time

# Function to create inherited table and measure time
def create_table_inherit(engine, table_class):
    start_time = timeit.default_timer()
    engine.create_table_inherit(table_class)
    elapsed_time = timeit.default_timer() - start_time
    return elapsed_time

if __name__ == "__main__":
    PROJECT_ROOT = os.path.abspath(os.path.join(
                      os.path.dirname(__file__), 
                      os.pardir)
    )
    connection_string = "postgresql://postgres:Qwerty22333@localhost:5432/postgres"
    
    engine, engine_creation_time = create_engine(connection_string)

    class Custom1(TableBase):
        var1 = String(type='VARCHAR', n=100)
        var2 = String(type='VARCHAR', n=100)
        var3 = String(type='VARCHAR', n=100)
        var4 = String(type='VARCHAR', n=100)
    
    class Custom2(TableBase):
        var1 = String(type='VARCHAR', n=100)
        var2 = String(type='VARCHAR', n=100)
        var3 = String(type='VARCHAR', n=100)
        var4 = String(type='VARCHAR', n=100)

    create_table_time = create_table(engine, Custom1)
    
    create_table_inherit_time = create_table_inherit(engine, Custom2)

    print("Time to create engine:", round(engine_creation_time, 5))
    print("Time to create table:", round(create_table_time, 5))
    print("Time to create inherited table:", round(create_table_inherit_time, 5))
