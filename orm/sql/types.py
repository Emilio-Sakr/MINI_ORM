from .. import exc

class Base:
    __orm__type__ = True

class String(Base):
    types = ['VARCHAR', 'CHAR', 'TEXT']

    def __init__(self, type='', n=0):
        if not type or type=='TEXT':
            self.sql_str = 'TEXT'
        else:
            mode = String._assert_type(type)
            n = String._assert_int(n)
            self.sql_str = f'{mode}({n})'

    @classmethod
    def _assert_type(cls, type):
        if type in cls.types:
            return type
        else:
            raise exc.ArgumentError('String type must be one of {}'.format(cls.get_string_types()))
    
    @classmethod
    def _assert_int(cls, n):
        if isinstance(n, int):
            return n
        else:
            raise exc.ArgumentError('String max value must of integer type')
        
    @classmethod
    def get_string_types(cls):
        return ', '.join(cls.types)
        
class Integer(Base):
    types = ['SMALLINT', 'SERIAL', 'INT']

    def __init__(self, type = ''):
        if not type or type=='INT':
            self.sql_str = 'INT'
        else:
            self.sql_str = Integer._assert_type(type)

    @classmethod
    def _assert_type(cls, type):
        if type in cls.types:
            return type
        else:
            raise exc.ArgumentError('Integer type must be one of {}'.format(cls.get_string_types()))
        
    @classmethod
    def get_string_types(cls):
        return ', '.join(cls.types)
    
class Boolean(Base):
    def __init__(self):
        self.sql_str = 'BOOLEAN'
    
class ForeignKey(Base):
    __orm__type__ = True

    def __init__(self, referenced_table, column):
        self.referenced_table = referenced_table
        self.column = column

    def get(self, name):
        self.sql_str = 'CONSTRAINT {} FOREIGN KEY ({}) REFERENCES {}'.format(name ,self.column, self.referenced_table)
        return self.sql_str
    
class Index(Base):
    __orm__type__ = True

    def __init__(self, *columns, **kwargs):
        self.unique = kwargs.pop('unique', False)
        self.columns = columns

    def get(self, name):
        column_list = ', '.join(self.columns)
        if self.unique:
            self.sql_str = f'CONSTRAINT {name} UNIQUE ({column_list})'
        else:
            self.sql_str = f'INDEX {name} ({column_list})'
        return self.sql_str

        
types = (String, Integer, Boolean)
special_types = (ForeignKey, Index)