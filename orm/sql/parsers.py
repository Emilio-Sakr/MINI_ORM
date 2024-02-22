from .types import type_list, Base
from .. import exc

class POSTGRESQL_PARSER:
    orm_types = type_list

    @classmethod
    def create_table(cls, table: object) -> str:
        create_table_statement = f"CREATE TABLE IF NOT EXISTS {table.__name__.lower()} ("
        create_table_statement += f"id SERIAL PRIMARY KEY, "
        attributes = []
        for attribute_name, attribute_value in table.__dict__.items():
            if attribute_name == 'id':
                continue #TODO handle id definition changes
            if not attribute_name.startswith("__"):
                if not isinstance(attribute_value, tuple):
                    sql_type = cls._assert_sql_type(attribute_value)
                    attributes.append(cls._parse_attribute(attribute_name, sql_type))
                else:
                    sql_type = cls._assert_sql_type(attribute_value[0])
                    constraints = attribute_value[1:]
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
    def _parse_attribute(cls, attribute_name: str, type: Base, constraints: list = []):
        if not constraints:
            return '{} {}'.format(attribute_name, type.sql_str)
        else:
            constraints_text = ' '.join(constraints)
            return '{} {} {}'.format(attribute_name, type.sql_str, constraints_text)


