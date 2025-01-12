from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.sentiment import SentimentData
from app.schemas.sentiment import SentimentCreate

product_router = APIRouter()


@product_router.get("/sentiments")
async def list_sentiments(db: Session = Depends(get_db)):
    return db.query(SentimentData).all()


@product_router.get("/sentiment/{sentiment_id}")
async def get_sentiment(sentiment_id: int, db: Session = Depends(get_db)):
    sentiment = db.query(SentimentData).filter(SentimentData.id == sentiment_id).first()
    if not sentiment:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        return sentiment


# id = Column(Integer, primary_key=True)
#     product_name = Column(String, ForeignKey("products.title"), nullable=False)
#     positive_count = Column(Integer, default=0)
#     neutral_count = Column(Integer, default=0)
#     negative_count = Column(Integer, default=0)
#     timestamp = Column


@product_router.post("/sentiment")
async def save_sentiment(sentiment: SentimentCreate, db: Session = Depends(get_db)):
    new_sentiment = SentimentData(
        product_name=sentiment.product_name,
        positive_count=sentiment.positive_count,
        neutral_count=sentiment.neutral_count,
        negative_count=sentiment.negative_count,
        timestamp=sentiment.timestamp,
    )
    db.add(new_sentiment)
    db.commit()
    db.refresh(new_sentiment)
    return new_sentiment


@product_router.delete("/sentiment/{sentiment_id}")
def delete_product(sentiment_id: int, db: Session = Depends(get_db)):
    sentiment = db.query(SentimentData).get(sentiment_id)
    if not sentiment:
        raise HTTPException(status_code=404, detail="Sentiment not found")
    else:
        db.delete(sentiment)
        db.commit()
        return {"detail": "Sentiment deleted successfully"}
