## Table of Contents

- [Introduction](#introduction)
- [Connecting to the database](#database-connection)
- [ORM Datatypes](#orm-datatypes)
- [Creating a table](#creating-a-table)
- [CRUD operations](#crud-operations)

## Introduction

This documentation provides a comprehensive guide for using the ORM (Object-Relational Mapping) library designed to interact with a PostgreSQL database. The library simplifies database operations by abstracting SQL queries into Python classes and methods.

## Database Connection

### Connection String Parameters:

The connection string contains information required to establish a connection to the PostgreSQL database. Here's a breakdown of typical parameters found in a connection string:

1. **Username**: The username used to authenticate with the database.
2. **Password**: The password associated with the specified username.
3. **Host**: The address of the database server.
4. **Port**: The port number on which the database server is listening for connections.
5. **Database Name**: The name of the database to connect to.

### Optional Attributes:

- logger (optional):
  If provided, this attribute allows you to pass a logger object to the Engine class for logging purposes. If not provided, the engine will not perform logging.

- min_pool_size (optional):
  The minimum pool size refers to the minimum number of connections that the connection pool should maintain. Setting a minimum pool size ensures that a certain number of connections are always available in the pool, reducing connection establishment overhead, default is 1.

- max_pool_size (optional):
  The maximum pool size specifies the maximum number of connections that the connection pool can hold at any given time. Once the maximum pool size is reached, further connection requests are rejected, default is 5.

### Initiating the Connection:

Once the connection string and optional attributes are defined, an Engine object is created to facilitate database interactions. The Engine class provides methods for establishing and managing connections to the database.

Here's how the connection process typically looks in code:

```python
# Define the connection string
connection_string = "postgresql://username:password@host:port/database_name"

# Create an Engine object with the connection string and optional parameters
engine = Engine(connection_string, min_pool_size=3, max_pool_size=10)
```

## ORM Datatypes

The ORM library provides several data types that facilitate defining database tables and their attributes. These data types include:

- String
- Integer
- Boolean
- ForeignKey
- Index

Each data type offers specific functionalities and options for defining the structure and constraints of database tables.
Data types are imported from orm.sql

### String:

The String data type represents text fields in database tables. It supports the following SQL types: 'VARCHAR', 'CHAR', and 'TEXT'. If no type is specified, the default is 'TEXT'.

Usage:

```python
# Define a VARCHAR string field with a maximum length of 255 characters
name = String(type='VARCHAR', n=255)

# Define a TEXT string field with no specified length limit (default)
description = String()
```

### Integer:

The Integer data type represents integer fields in database tables. It supports the SQL types: 'SMALLINT', 'SERIAL', and 'INT'. If no type is specified, the default is 'INT'.

Usage:

```python
# Define an integer field (default type: INT)
age = Integer()

# Define a small integer field
quantity = Integer(type='SMALLINT')
```

### Boolean:

The Boolean data type represents boolean fields in database tables. The default value is False.

Usage:

```python
# Define a boolean field with default value False
is_active = Boolean()
```

### ForeignKey:

The ForeignKey data type represents a foreign key constraint in database tables. It establishes a relationship between two tables by referencing the primary key of another table.

Usage:

```python
# Define a foreign key constraint referencing the 'id' column of the 'authors' table

author_id = ForeignKey('authors(id)', 'author_id')
```

### Index:

The Index data type represents an index in database tables. Indexes are used to improve the performance of queries by speeding up data retrieval.

Usage:

```python
# Define an index on the 'email' column with unique constraint (default: unique=False)
email_index = Index('email', unique=True)
```

## Creating a Table

Tables in the ORM library allow you to define database table structures and interact with them using Python classes. This comprehensive guide walks you through the process of creating tables, binding them to the engine, and performing various CRUD operations.

### Define Table Structure

Begin by defining the structure of your table by creating a Python class inheriting from TableBase from orm.sql. Each attribute within the class represents a column in the table, defined using ORM data types such as String, Integer, Boolean, ForeignKey, and Index.

```python
from orm.sql import TableBase

class Usernames(TableBase):
    matricule = (Integer(type='INT'), 'UNIQUE')
    username = String(type='VARCHAR', n=100)
    email = String(type='VARCHAR', n=200)
    password = (String('VARCHAR', n=100), 'CHECK ($ <> username AND CHAR_LENGTH($) >= 8)')
```

- For a single datatype without constraints, simply specify the datatype directly.
- When introducing constraints, wrap the datatype in a tuple along with the desired constraints.
- In check constraints, represent column names with "$" instead of the actual column name.

### Create Tables

- Standalone Table
  Use the create_table method of the Engine class to explicitly create a standalone table in the database.

```python
engine.create_table(MyTable)
```

- Inherited Table
  Use the create_table_inherit method of the Engine class when creating a table that inherits attributes or structure from another table. Provide a subclass of TableBase as an argument to inherit attributes from another table class.

```python
engine.create_table_inherit(MySubTable)
```

### Bind Tables to Engine

After creating the table(s), bind them to the engine using the connect_to method of the table class. This step is essential as it establishes the connection between the table(s) and the engine, enabling the engine to perform CRUD operations (Create, Read, Update, Delete) on the table(s).

```python
MyTable.connect_to(engine)
```

## CRUD Operations

### Inserting Data:

To insert data into a table, you can use the insert method of the corresponding table class. You can insert either a single record or multiple records at once.

```python
# Single Record Insertion
TableClass.insert(column1=value1, column2=value2, ...)

# Multiple Records Insertion
data = [
    {'column1': value1, 'column2': value2, ...},
    {'column1': value1, 'column2': value2, ...},
    ...
]
TableClass.insert_all(data)
```

### Deleting Data:

To delete data from a table, you can use the delete method of the corresponding table class. You can delete specific records based on conditions or delete all records from the table.

```python
# Delete Specific Records
TableClass.delete(filter_by='condition')

# Delete All Records
TableClass.delete()
```

### Updating Data:

To update data in a table, you can use the update method of the corresponding table class. You can specify the columns and their new values to be updated, along with optional filtering conditions.

```python
# Update Records
TableClass.update(filter_by='condition', column1=new_value1, column2=new_value2, ...)
```

### Querying Data:

To retrieve data from a table, you can use the select method of the corresponding table class. You can specify the columns to retrieve, apply filtering conditions, order the results, and limit the number of returned records.

```python
# Retrieve All Records
TableClass.select()

# Retrieve Specific Columns
TableClass.select('column1', 'column2', ...)

# Apply Filtering Conditions
TableClass.select(filter_by={'column1': 'value1', 'column2': 'value2'})

# Order the Results
TableClass.select(order_by='column ASC')

# Limit the Number of Returned Records
TableClass.select(limit=10)

# Offset the Results (for pagination)
TableClass.select(offset=10)
```

### Usage Guidelines:

Filtering conditions allow you to retrieve specific data from your database based on certain criteria. Here's a breakdown of the different formats:

- String: You can directly specify the conditions as a string where you define the criteria using SQL syntax. For example, 'age > 2 AND name = "Marc"' means you want to retrieve records where the age is greater than 2 and the name is "Marc".

- Tuple or List: This format provides flexibility and readability. You can pass multiple conditions as elements of a tuple or list. Each element represents a separate condition. For instance, ['age > 2', 'name = "Marc"'] or ('age > 2', 'name = "Marc"') allows you to specify more than one condition.

- Dictionary with LIKE: When using a dictionary, you can use the LIKE keyword to perform wildcard searches, typically for text matching. For example, {'name': 'M%'} will match names starting with 'M'. This is particularly useful for pattern matching where you want to retrieve records based on partial string matches.
