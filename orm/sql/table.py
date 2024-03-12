from .. import exc

class TableBase:
    __engine = None  
    
    @classmethod
    def connect_to(cls, engine_instance):
        cls.__engine = engine_instance
    
    @classmethod
    def _check_args(cls, *args, **kwargs):
        '''
        Checks if provided arguments are inside the table.

        If kwargs are provided: check if keys are in the table attributes
        If args are provided: expects chunks in args to contain dictionaries that have keys that are in the table attributes
        '''
        for key in kwargs.keys():
            if not hasattr(cls, key):
                raise exc.ResourceError(f"Unknown attribute '{key}' provided for '{cls.__name__}'")
        
        for chunks in args:
            length = len(chunks[0])
            for chunk in chunks:
                if len(chunk) != length:
                    raise exc.ResourceError('Records should be of the same lenght')
                for key in chunk.keys():
                    if not hasattr(cls, key):
                        raise exc.ResourceError(f"Unknown attribute '{key}' provided for '{cls.__name__}'")
    
    @classmethod
    def _ensure_engine_connected(cls):
        if cls.__engine is None:
            raise exc.ResourceError("No engine connected")
    
    @classmethod
    def insert(cls, **columns):
        cls._ensure_engine_connected()
        cls._check_args(**columns)
        cls.__engine.insert(cls, **columns)

    @classmethod
    def insert_all(cls, records: list[dict]):
        cls._ensure_engine_connected()
        cls._check_args(records)
        cls.__engine.insert_all(cls, records)
    
    @classmethod
    def update(cls, filter_by, **columns):
        cls._ensure_engine_connected()
        cls._check_args(**columns)
        cls.__engine.update(cls, filter_by, **columns)
    
    @classmethod
    def delete(cls, filter_by):
        cls._ensure_engine_connected()
        cls.__engine.delete(cls, filter_by)

    @classmethod
    def select(cls, columns='*', **constraints):
        cls._ensure_engine_connected()
        return cls.__engine.select(cls, columns, **constraints)