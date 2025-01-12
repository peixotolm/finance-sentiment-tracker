from datetime import datetime

from pydantic import BaseModel


class SentimentBase(BaseModel):
    product_name: str
    positive_count: int
    neutral_count: int
    negative_count: int
    timestamp: datetime


class SentimentCreate(SentimentBase):
    pass


class Sentiment(SentimentBase):
    id: int

    class Config:
        from_attributes = True
