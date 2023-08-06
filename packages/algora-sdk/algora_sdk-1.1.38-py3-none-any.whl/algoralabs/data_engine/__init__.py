from enum import Enum
from typing import Optional, Union, List

from pydantic import BaseModel

from algoralabs.common.enum import FieldType


class FieldFill(Enum):
    NULL = 'NULL'
    ZERO = 'ZERO'
    PREVIOUS = 'PREVIOUS'
    NEXT = 'NEXT'


class FieldMetric(BaseModel):
    name: str
    type: FieldType
    length: int
    num_null: int
    num_zero: int
    min: Optional[Union[float, int]]
    max: Optional[Union[float, int]]
    std_dev: Optional[float]


class FieldOverride(BaseModel):
    name: str
    type: Optional[FieldType] = None
    fill: Optional[FieldFill] = None


class TransformOverride(BaseModel):
    fields: List[FieldOverride] = []
    default_fill: FieldFill = FieldFill.PREVIOUS
