from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class StockData(Base):
    __tablename__ = "stock_data"

    id = Column(Integer, primary_key=True)
    product_name = Column(String, ForeignKey("products.title"), nullable=False)
    price = Column(Float)
    open_price = Column(Float)
    close_price = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="stock_data")
