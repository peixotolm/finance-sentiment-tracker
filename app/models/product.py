from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.core.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String)

    # Define relationships using model names as strings to avoid circular imports
    sentiments = relationship(
        "SentimentData", order_by="SentimentData.id", back_populates="product"
    )
    stock_data = relationship(
        "StockData", order_by="StockData.id", back_populates="product"
    )
