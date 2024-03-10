from .types import type_list, Base
from .. import exc

class POSTGRESQL_PARSER:
    orm_types = type_list

    @classmethod
    def create_table(cls, table: object) -> str:
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
    def _parse_check(cls, attribute_name: str, constraints: list[str]):
        for index, cons in enumerate(constraints):
            if 'check' in cons.lower():
                constraints[index] = cons.replace('$', attribute_name)

    @classmethod
    def _parse_attribute(cls, attribute_name: str, type: Base, constraints: list[str] = []):
        if not constraints:
            return '{} {}'.format(attribute_name, type.sql_str)
        else:
            cls._parse_check(attribute_name, constraints)
            constraints_text = ' '.join(constraints)
            return '{} {} {}'.format(attribute_name, type.sql_str, constraints_text)

    @classmethod
    def insert(cls, table, **kwargs):
        columns = ', '.join(kwargs.keys())
        values = ', '.join(f"'{value}'" if isinstance(value, str) else str(value) for value in kwargs.values())
        return f"INSERT INTO {table.__name__} ({columns}) VALUES ({values})"
    
    @classmethod
    def update(cls, table, filter_clause, **kwargs):
        set_clause = ', '.join(f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}" for key, value in kwargs.items())        
        sql_update = f"UPDATE {table.__name__} SET {set_clause} WHERE {filter_clause};"
        return sql_update
    
    @classmethod
    def delete(cls, table, filter_clause):
        sql_delete = f"DELETE FROM {table.__name__} WHERE {filter_clause};"
        return sql_delete

def has_primary_key(cls):
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if isinstance(attr, tuple) and 'PRIMARY KEY' in attr:
            return True
    return False