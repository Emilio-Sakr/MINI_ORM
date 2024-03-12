from .types import type_list, Base, ForeignKey, Index
from .. import exc

class POSTGRESQL_PARSER:
    orm_types = type_list

    @classmethod
    def create_table(cls, table: object) -> str:
        """
        Generate an SQL CREATE TABLE statement for the specified table object.

        Args:
            table (class): The table class representing the table schema.

        Returns:
            str: An SQL CREATE TABLE statement.

        This method constructs a CREATE TABLE statement based on the attributes of the provided table object.
        It first checks if the table has a primary key defined. If not, it adds a default primary key named 'id' or 'rowid'.
        Then, it iterates over the attributes of the table object to extract attribute names, types, and constraints.
        Finally, it combines all attribute definitions to form the complete CREATE TABLE statement.
        """

        create_table_statement = f"CREATE TABLE IF NOT EXISTS {table.__name__.lower()} ("
        
        if not has_primary_key(table):
            if 'id' in dir(table):
                create_table_statement += f"rowid SERIAL PRIMARY KEY, "
            elif 'rowid' in dir(table):
                create_table_statement += f"pk_ SERIAL PRIMARY KEY, "
            else:
                create_table_statement += f"id SERIAL PRIMARY KEY, "

        attributes = []
        for attribute_name, attribute_value in table.__dict__.items():
            if not attribute_name.startswith("__"):
                if not isinstance(attribute_value, tuple):
                    sql_type = cls._assert_sql_type(attribute_value)
                    attributes.append(cls._parse_attribute(attribute_name, sql_type))
                else:
                    sql_type = cls._assert_sql_type(attribute_value[0])
                    constraints = list(attribute_value[1:])
                    attributes.append(cls._parse_attribute(attribute_name, sql_type, constraints))

        create_table_statement += ", ".join(attributes)
        create_table_statement += ")"
        return create_table_statement

    @classmethod
    def _assert_sql_type(cls, type_):
        for orm_type in cls.orm_types:
            if isinstance(type_, orm_type):
                return type_
        raise exc.ArgumentError('{} is not a orm type'.format(type(type_)))
    
    @classmethod
    def _parse_check(cls, attribute_name: str, constraints: list[str]) -> None:
        for index, cons in enumerate(constraints):
            if 'check' in cons.lower():
                constraints[index] = cons.replace('$', attribute_name)

    @classmethod
    def _parse_attribute(cls, attribute_name: str, type: Base, constraints: list[str] = []) -> str:
        if isinstance(type, (ForeignKey, Index)):
            return type.get(attribute_name)
        elif not constraints:
            return '{} {}'.format(attribute_name, type.sql_str)  
        else:
            cls._parse_check(attribute_name, constraints)
            constraints_text = ' '.join(constraints)
            return '{} {} {}'.format(attribute_name, type.sql_str, constraints_text)

    @classmethod
    def insert(cls, table, **columns) -> str:
        """
        Generates an SQL INSERT statement for inserting one record into the specified table.

        Args:
            table (class): The table class representing the table into which the record will be inserted.
            **columns: Column names and their values.

        Returns:
            str: The SQL INSERT statement.
        """

        columns_str = ', '.join(columns.keys())
        values = ', '.join(f"'{value}'" if isinstance(value, str) else str(value) for value in columns.values())
        return f"INSERT INTO {table.__name__} ({columns_str}) VALUES ({values})"
    
    @classmethod
    def insert_all(cls, table, records):
        """
        Construct an SQL INSERT statement for inserting multiple records into the specified table.

        Args:
            table (class): The table class representing the table into which the records will be inserted.
            records (list of dict): List of dictionaries, where each dictionary
                                    represents the data for one record to be inserted.
                                    Example: [{'title': 'Book1', 'author': 'Author1', ...},
                                            {'title': 'Book2', 'author': 'Author2', ...}, ...]

        Returns:
            str: An SQL INSERT statement for inserting multiple records.
        """

        columns = ', '.join(records[0].keys())
        values = ', '.join(
            f"({', '.join(f'{value!r}' if isinstance(value, str) else str(value) for value in record.values())})"
            for record in records
        )
        return f"INSERT INTO {table.__name__} ({columns}) VALUES {values};"
    
    @classmethod
    def update(cls, table, filter_by, **columns) -> str:
        """
        Construct an SQL UPDATE statement for updating records in the specified table.

        Args:
            table (class): The table class representing the table to be updated.
            filter_by: Filtering conditions.
            **columns: Keyword arguments representing the column names and new values to be updated.

        Returns:
            str: An SQL UPDATE statement.
        """
         
        set_clause = ', '.join(f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}" for key, value in columns.items())        
        sql_update = f"UPDATE {table.__name__} SET {set_clause}"

        if filter_by:
            sql_filter = cls._filter(filter_by)
            sql_update += sql_filter

        sql_update += ";"
        return sql_update
    
    @classmethod
    def delete(cls, table, filter_by):
        """
        Construct an SQL DELETE statement for deleting records from the specified table.

        Args:
            table (class): The table class representing the table from which records will be deleted.
            filter_by: Filtering conditions.

        Returns:
            str: The SQL DELETE statement.
        """

        sql_delete = f"DELETE FROM {table.__name__}"

        if filter_by:
            sql_filter = cls._filter(filter_by)
            sql_delete += sql_filter

        sql_delete += ";"
        return sql_delete
    
    @classmethod
    def select(cls, table, columns, **constraints):
        """
        Generates an SQL SELECT statement to query data from the specified table

        Args:
            table (class): The table class representing the table from which records will be returned.
            columns (str or list): Columns to select.
            **constraints: Additional constraints like filter_by, order_by, limit.

        Returns:
            str: The SQL SELECT statement.

        This method generates an SQL SELECT statement for querying records from the table.
        It constructs the SELECT statement with optional filtering, ordering, and limiting conditions.
        """

        filter_by = constraints.get('filter_by', None)
        order_by = constraints.get('order_by', None)
        limit = constraints.get('limit', None)

        if isinstance(limit, (list, tuple)) and len(limit) != 2:
            raise exc.ArgumentError('Limit instance must have 2 values not {}'.format(len(limit)))

        columns = cls._columns(columns)

        sql_select = f"SELECT {columns} FROM {table.__name__}"

        if filter_by:
            sql_filter = cls._filter(filter_by)
            sql_select += sql_filter

        if order_by:
            sql_order = cls._order_by(order_by)
            sql_select += sql_order

        if limit:
            sql_limit = cls._limit(limit)
            sql_select += sql_limit

        sql_select += ";"
        return sql_select

    @classmethod
    def _columns(cls, columns) -> str:
        if isinstance(columns, (list, tuple)):
            columns = ', '.join(columns)
        elif isinstance(columns, str):
            columns = ', '.join(columns.split(' '))
        else:
            raise exc.ArgumentError('Provided columns in wrong format')
        return columns

    @classmethod
    def _filter(cls, filter_by) -> str:
        sql_filter = ''
        if isinstance(filter_by, list) or isinstance(filter_by, tuple):
            filter_conditions = ' AND '.join(filter_by)
            sql_filter += f" WHERE {filter_conditions}"

        elif filter_by and isinstance(filter_by, dict):
            where_conditions = []
            for column, pattern in filter_by.items():
                where_conditions.append(f"{column} LIKE '{pattern}'")

            filter_conditions = ' AND '.join(where_conditions)
            sql_filter += f" WHERE {filter_conditions}"

        elif filter_by and filter_by != '*':
            sql_filter += f" WHERE {filter_by}"

        return sql_filter
    
    @classmethod
    def _order_by(cls, order_by) -> str:
        sql_order = ''
        if isinstance(order_by, (list, tuple)):
            order_conditions = ', '.join(order_by)
            sql_order += f" ORDER BY {order_conditions}"
        else:
            sql_order += f" ORDER BY {order_by}"
        return sql_order
    
    @classmethod
    def _limit(cls, limit):
        sql_limit = ''
        if isinstance(limit, (list, tuple)) and len(limit) == 2:
            sql_limit += f" LIMIT {limit[0]}, {limit[1]}"

        else:
            sql_limit += f" LIMIT {limit}"
        return sql_limit

def has_primary_key(cls):
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if isinstance(attr, tuple):
            for item in attr:
                if isinstance(item, str) and 'primary key' in item.lower():
                    return True
    return False