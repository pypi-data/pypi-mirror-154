from enum import Enum
from typing import Optional

from pydantic import BaseModel


class BacktestType(Enum):
    STRATEGY = 'STRATEGY'
    BACKTEST = 'BACKTEST'


class BacktestStatus(Enum):
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    CANCELED = 'CANCELED'


class BacktestRequest(BaseModel):
    strategy_id: str
    type: BacktestType
    status: BacktestStatus
    start_date: int
    end_date: int
    portfolio: str  # TODO replace with portfolio object in Quant SDK


class BacktestResponse(BaseModel):
    id: str
    strategy_id: str
    type: BacktestType
    status: BacktestStatus
    start_date: int
    end_date: int
    portfolio: str  # TODO replace with portfolio object in Quant SDK
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]


class BacktestViewResponse(BaseModel):
    id: str
    strategy_id: str
    strategy_name: str
    type: BacktestType
    status: BacktestStatus
    start_date: int
    end_date: int
    portfolio: str  # TODO replace with portfolio object in Quant SDK
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]


class BacktestEventType(Enum):
    PORTFOLIO = 'PORTFOLIO'
    CASH_PAYMENT = 'CASH_PAYMENT'


class BacktestEvent(BaseModel):
    backtest_id: str
    backtest_type: BacktestEventType


class CashPaymentRequest(BaseModel):
    backtest_id: str
    payment_date: int
    side: str
    type: str
    amount: float
    position_id: Optional[str]
    currency: Optional[str]


class PortfolioStateRequest(BaseModel):
    backtest_id: str
    date: int
    valuation: float
    pnl: float
    portfolio: str


class CashPaymentResponse(BacktestEvent):
    id: str
    backtest_id: str
    backtest_type: BacktestEventType
    payment_date: int
    side: str
    type: str
    amount: float
    position_id: Optional[str]
    currency: Optional[str]
    created_at: int


class PortfolioStateResponse(BacktestEvent):
    id: str
    backtest_id: str
    backtest_type: BacktestEventType
    date: int
    valuation: float
    pnl: float
    portfolio: str
    created_at: int
