import sys
import uuid

import json

from sqlalchemy import Column, Integer, DateTime, String, engine_from_config
from sqlalchemy.dialects.postgresql import (
    UUID as PgUUID,
    JSON as PgJSON,
    JSONB as PgJSONB,
    ARRAY as PgARRAY,
)
from sqlalchemy.types import (
    TypeDecorator,
    Concatenable,
    UserDefinedType,
    CHAR,
    TEXT,
    UnicodeText,
)

if sys.version_info[0] > 2:
    basestring = (str, bytes)


class UUID(TypeDecorator):
    """
    Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses CHAR(32), storing as
    stringified hex values.
    """

    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PgUUID(False))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value

        if isinstance(value, basestring):
            value = uuid.UUID(value)
        elif not isinstance(value, uuid.UUID):
            raise ValueError('%r is not a valid UUID.' % value)

        # mysql should be value.bytes if BINARY
        return str(value)

    def process_result_value(self, value, dialect):
        # mysql should convert bytes in uuid if BINARY
        return value
