from datetime import datetime
from pydantic import BaseModel


class StockBase(BaseModel):
    product_name: str
    price: float
    open_price: float
    close_price: float
    high: float
    low: float
    volume: float
    date: datetime


class StockCreate(StockBase):
    pass


class Stock(StockBase):
    id: int

    class Config:
        from_attributes = True
