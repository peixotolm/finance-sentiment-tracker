from datetime import datetime
from pydantic import BaseModel


class SentimentBase(BaseModel):
    product_name: str
    positive_count: int
    neutral_count: int
    negative_count: int
    timestamp: datetime = datetime.utcnow()  # Default value


class SentimentCreate(SentimentBase):
    pass


class Sentiment(SentimentBase):
    id: int

    class Config:
        orm_mode = True
