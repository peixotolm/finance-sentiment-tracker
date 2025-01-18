from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.base import Base
from app.models.product import Product  # noqa: F401
from app.models.sentiment import SentimentData  # noqa: F401
from app.models.stock import StockData  # noqa: F401

DATABASE_URL = config("DATABASE_URL", default="sqlite:///test.db")

try:
    engine = create_engine(DATABASE_URL, echo=True)
except Exception as e:
    raise RuntimeError("Invalid DATABASE_URL") from e

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db():
    with SessionLocal() as db:
        yield db
