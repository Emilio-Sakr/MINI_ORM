import re
from typing import Optional

from .. import exc

class URL:
    supported_servers = ['postgresql']

    def __init__(self, server, username, password, host, port, database, pool) -> "URL":
        self.server = server
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.pool = pool

    @classmethod
    def create(
        cls,
        server: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        pool: Optional[dict] = {}
    ) -> "URL":
        
        return URL(
            cls._assert_server(server),
            cls._assert_none_str(username, "username"),
            password,
            cls._assert_none_str(host, "host"),
            cls._assert_port(port),
            cls._assert_none_str(database, "database"),
            pool
        )
    
    @classmethod
    def _assert_server(cls, drivername: str):
        if drivername not in URL.supported_servers:
            raise exc.ArgumentError('{} servers are not supported'.format(drivername))
        else: 
            return drivername
    
    @classmethod
    def _assert_str(cls, value: str, name: str) -> str:
        if not isinstance(value, str):
            raise ValueError('{} must be a string'.format(name))
        else: 
            return value
    
    @classmethod
    def _assert_none_str(cls, value: Optional[str], name: str) -> Optional[str]:
        if value is None:
            return value
        else: 
            return cls._assert_str(value, name)

    @classmethod
    def _assert_port(cls, port: Optional[int]) -> Optional[int]:
        if port is None:
            return port
        else: 
            if not isinstance(port, int) or (port <= 0 or port >= 65536):
                raise TypeError('Port must be an integer between 1 and 65536')
            return port

def url_parser(connection_string: str, **kwargs) -> URL:
    pattern = re.compile(
        r"""
        (?P<name>[\w\+]+)://
        (?P<username>[^:/]+):
        (?P<password>[^@]+)@
        (?P<host>[^:/]+):
        (?P<port>\d+)/
        (?P<database>\w+)
        """,
        re.X,
    )

    match = pattern.match(connection_string)

    if match:
        components = match.groupdict()

        components.update({'pool': {}})
        pool_componants = ['pool_size', 'max_overflow', 'pool_timeout']
        for key, value in kwargs.items():
            if key in pool_componants:
                components['pool'][key] = value

        name = components.pop("name")

        if components["port"]:
            components["port"] = int(components["port"])

        return URL.create(name, **components) 
    else:
        raise exc.ArgumentError('Connection URL does not match ORM specifications')