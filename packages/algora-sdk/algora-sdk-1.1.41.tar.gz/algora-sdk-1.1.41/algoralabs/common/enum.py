from enum import Enum
from pydantic import BaseModel


class FieldType(Enum):
    BOOLEAN = 'BOOLEAN'
    DOUBLE = 'DOUBLE'
    INTEGER = 'INTEGER'
    TEXT = 'TEXT'
    TIMESTAMP = 'TIMESTAMP'
    DATETIME = 'DATETIME'
    UNKNOWN = 'UNKNOWN'


class Field(BaseModel):
    logical_name: str
    type: FieldType
