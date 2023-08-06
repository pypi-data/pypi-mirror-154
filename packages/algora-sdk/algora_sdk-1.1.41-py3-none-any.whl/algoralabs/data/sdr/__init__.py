from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel


class AssetClass(Enum):
    COMMODITY = "commodity"
    CREDIT = "credit"
    EQUITY = "equity"
    FOREX = "forex"
    RATES = "rates"


class Repository(Enum):
    CME = "CME"
    DTCC = "DTCC"
    ICE = "ICE"


class LogicalDisplayName(BaseModel):
    display_name: str
    logical_name: str


class DateRange(BaseModel):
    start_date: str
    end_date: str
    enabled: bool


class APIFieldFilter(BaseModel):
    logical_display: LogicalDisplayName
    operator: str  # operator can be "NOT_IN" or "IN" or "NOT_EQUAL" or "EQUAL" or "GTE" or "GT" or "LTE" or "LT"
    selected_values: List[str]


class FieldFilter(BaseModel):
    field: str
    operator: str  # operator can be "NOT_IN" or "IN" or "NOT_EQUAL" or "EQUAL" or "GTE" or "GT" or "LTE" or "LT"
    selected_values: List[str]


class DataFilter(BaseModel):
    date_range: Optional[DateRange]
    filters: List[Union[FieldFilter, APIFieldFilter]]
