'''
All ORM Exceptions are defined in here
'''


class ORMException(Exception):
    """Generic error class."""
    code = 0

    def __init__(self, message):
        self.message = message
        self.code = self.__class__._get_code()
        super().__init__(self.message)

    @classmethod
    def _get_code(cls):
        return cls.code

    def __str__(self):
        return f"{self.__class__.__name__} ({self.code}): {self.message}"

class ArgumentError(ORMException):
    """
    Raised when an invalid or conflicting function argument is supplied.

    This error generally corresponds to construction time state errors that are user invoked.
    """
    code = 101

class ConstructionError(ORMException):
    """
    Raised when an fatal error occurs in ORM construction steps.

    This error generally corresponds to construction time state errors that are not user invoked.
    """
    code = 102

class ResourceError(ORMException):
    """
    Raised when an resource is not accessible.
    """
    code = 201

