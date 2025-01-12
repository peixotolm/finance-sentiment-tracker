from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.sentiment import SentimentData
from app.models.stock import StockData


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String)


Product.sentiments = relationship(
    "SentimentData", order_by=SentimentData.id, back_populates="product"
)
Product.stock_data = relationship(
    "StockData", order_by=StockData.id, back_populates="product"
)
