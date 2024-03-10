from .. import exc

class TableBase:
    __engine = None  
    
    @classmethod
    def connect_to(cls, engine_instance):
        cls.__engine = engine_instance
    
    @classmethod
    def _check_args(cls, **kwargs):
        '''
        Checks if provided arguments are inside the table
        '''
        for key in kwargs.keys():
            if not hasattr(cls, key):
                raise exc.ResourceError(f"Unknown attribute '{key}' provided for '{cls.__name__}'")
    
    @classmethod
    def _ensure_engine_connected(cls):
        if cls.__engine is None:
            raise exc.ResourceError("No engine connected")
    
    @classmethod
    def insert(cls, **kwargs):
        cls._ensure_engine_connected()
        cls._check_args(**kwargs)
        cls.__engine.insert(cls, **kwargs)
    
    @classmethod
    def update(cls, filter_clause, **kwargs):
        cls._ensure_engine_connected()
        cls._check_args(**kwargs)
        cls.__engine.update(cls, filter_clause, **kwargs)
    
    @classmethod
    def delete(cls, filter_clause):
        cls._ensure_engine_connected()
        cls.__engine.delete(cls, filter_clause)