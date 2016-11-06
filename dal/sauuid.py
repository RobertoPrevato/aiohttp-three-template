from sqlalchemy import types
from sqlalchemy.dialects.mysql.base import MSBinary
import uuid


class UUID(types.TypeDecorator):
    """
    Implements UUID type for SqlAlchemy.

    By Tom Willis http://stackoverflow.com/users/67393/tom-willis
    http://stackoverflow.com/a/812363
    """
    impl = MSBinary
    def __init__(self):
        self.impl.length = 16
        types.TypeDecorator.__init__(self,length=self.impl.length)

    def process_bind_param(self,value,dialect=None):
        if value and isinstance(value,uuid.UUID):
            return value.bytes
        elif value and not isinstance(value,uuid.UUID):
            raise ValueError("value %s is not a valid uuid.UUID" % value)
        else:
            return None

    def process_result_value(self,value,dialect=None):
        if value:
            return uuid.UUID(bytes=value)
        else:
            return None

    def is_mutable(self):
        return False
