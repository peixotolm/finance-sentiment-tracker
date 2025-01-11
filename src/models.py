from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer)
    title = Column(String, primary_key=True, unique=True, nullable=False)


class SentimentData(Base):
    __tablename__ = "sentiments"

    id = Column(Integer, primary_key=True)
    product_name = Column(Integer, ForeignKey("products.title"), nullable=False)
    positive_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="sentiments")


class StockData(Base):
    __tablename__ = "stock_data"

    id = Column(Integer, primary_key=True)
    product_name = Column(Integer, ForeignKey("products.title"), nullable=False)
    price = Column(Float)
    open_price = Column(Float)
    close_price = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="stock_data")


Product.sentiments = relationship(
    "SentimentData", order_by=SentimentData.id, back_populates="product"
)
Product.stock_data = relationship(
    "StockData", order_by=StockData.id, back_populates="product"
)
