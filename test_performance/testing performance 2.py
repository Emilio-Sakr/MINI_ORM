import os
import sys
import timeit

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
from orm.sql import *
from orm import Engine

# Function to create engine and measure time
def create_engine(connection_string):
    start_time = timeit.default_timer()
    engine = Engine(connection_string, min_pool_size=3)
    elapsed_time = timeit.default_timer() - start_time
    return engine, elapsed_time

# Function to execute a query and measure time
def execute_query(engine, query):
    start_time = timeit.default_timer()
    result = engine.execute(query)
    elapsed_time = timeit.default_timer() - start_time
    return result, elapsed_time

if __name__ == "__main__":
    connection_string = "postgresql://postgres:Qwerty22333@localhost:5432/postgres"

    engine, engine_creation_time = create_engine(connection_string)

    class Custom(TableBase):
        var1 = String(type='VARCHAR', n=100)
        var2 = String(type='VARCHAR', n=100)
        var3 = String(type='VARCHAR', n=100)

    engine.create_table(Custom)
    Custom.connect_to(engine)

    # Measure time for individual insertion of 10,000 records
    Custom.delete('*')
    start_time_insert = timeit.default_timer()
    for i in range(10000):
        Custom.insert(var1=f"Data{i}", var2=f"Data{i}", var3=f"Data{i}")
    individual_insertion_time = timeit.default_timer() - start_time_insert

    # Measure time for bulk insertion of 10,000 records
    Custom.delete('*')
    data = [{'var1': f"Data{i}", 'var2': f"Data{i}", 'var3': f"Data{i}"} for i in range(10000)]
    start_time_insert_all = timeit.default_timer()
    Custom.insert_all(data)
    bulk_insertion_time = timeit.default_timer() - start_time_insert_all

    # Measure time for updating all records
    start_time_update_all = timeit.default_timer()
    Custom.update('*', var1 = 'new data')
    update_all_time = timeit.default_timer() - start_time_update_all

    # Measure time for selecting all records
    start_time_select_all = timeit.default_timer()
    result_select_all = Custom.select('*')
    select_all_time = timeit.default_timer() - start_time_select_all

    # Measure time for deleting all records
    start_time_delete_all = timeit.default_timer()
    Custom.delete('*')
    delete_all_time = timeit.default_timer() - start_time_delete_all

    print("Time to create engine:", round(engine_creation_time, 5))
    print("Time for individual insertion of 10 000 records:", round(individual_insertion_time, 5))
    print("Time for bulk insertion of 10 000 records:", round(bulk_insertion_time, 5))
    print("Time for updating of 10 000 records:", round(update_all_time, 5))
    print("Time for selecting of 10 000 records:", round(select_all_time, 5))
    print("Time for deleting of 10 000 records:", round(delete_all_time, 5))
