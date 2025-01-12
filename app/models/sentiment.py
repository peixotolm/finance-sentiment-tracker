from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class SentimentData(Base):
    __tablename__ = "sentiments"

    id = Column(Integer, primary_key=True)
    product_name = Column(String, ForeignKey("products.title"), nullable=False)
    positive_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="sentiments")
