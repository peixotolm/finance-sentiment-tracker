from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

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
