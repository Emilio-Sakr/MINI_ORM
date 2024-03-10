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
    


type_list = [String, Integer]