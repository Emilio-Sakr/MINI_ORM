from lib import url_parser, ConnectionPool

connection_string = "postgresql://postgres:Qwerty22333@localhost:5432/postgres"
url = url_parser(connection_string)
pool = ConnectionPool(url, **url.pool)

for _ in range(1):
    connection = pool.acquire()
    if connection:
            print("Acquired connection:", connection)
            sql_create_table = """
            CREATE TABLE IF NOT EXISTS example_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INT
            );
            """
            connection.execute_query(sql_create_table)
            
            # Check if the table was created successfully
            table_exists_query = """
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = 'example_table'
            );
            """
            table_exists = connection.execute_query(table_exists_query)[0][0]
            print(table_exists)

            # Simulate using the connection
            # For example, execute a query
            # connection.execute_query("SELECT * FROM table_name")
            pool.release(connection)
            print("Released connection:", connection)
