import os
import sys
import timeit
import time
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from orm.sql import *
from orm import Engine

# Function to create engine and measure time
def create_engine(connection_string, min_pool_size):
    start_time = timeit.default_timer()
    engine = Engine(connection_string, min_pool_size=min_pool_size)
    elapsed_time = timeit.default_timer() - start_time
    return engine, elapsed_time

if __name__ == "__main__":
    connection_string = "postgresql://postgres:Qwerty22333@localhost:5432/postgres"
    
    # Define different min_pool_sizes to test
    min_pool_sizes = [3, 5, 10, 20, 30, 40, 50, 70]

    for min_pool_size in min_pool_sizes:
        engine, engine_creation_time = create_engine(connection_string, min_pool_size)
        time.sleep(5)
        engine.close()
        print(f"Time to create engine with min_pool_size={min_pool_size}: {round(engine_creation_time, 5)} seconds")
