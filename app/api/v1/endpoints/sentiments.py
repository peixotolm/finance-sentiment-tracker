from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.product import Product
from app.models.sentiment import SentimentData
from app.schemas.sentiment import SentimentCreate
from app.core.logging_conf import logger

sentiment_router = APIRouter()


@sentiment_router.get("/sentiments")
async def list_sentiments(db: Session = Depends(get_db)):
    """Retrieve all sentiment records."""
    return db.query(SentimentData).all()


@sentiment_router.get("/sentiments/{sentiment_id}")
async def get_sentiment(sentiment_id: int, db: Session = Depends(get_db)):
    """Retrieve a sentiment by ID."""
    sentiment = db.query(SentimentData).filter(SentimentData.id == sentiment_id).first()
    if not sentiment:
        raise HTTPException(status_code=404, detail="Sentiment not found")
    return sentiment


@sentiment_router.post("/sentiments")
async def save_sentiment(sentiment: SentimentCreate, db: Session = Depends(get_db)):
    # Check if the product exists
    product = db.query(Product).filter(Product.title == sentiment.product_name).first()
    logger.info(f"Product: {product}")
    if not product:
        raise HTTPException(
            status_code=400,
            detail=f"Product with title '{sentiment.product_name}' does not exist.",
        )

    # Create the SentimentData entry
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


@sentiment_router.delete("/sentiment/{sentiment_id}")
async def delete_sentiment(sentiment_id: int, db: Session = Depends(get_db)):
    """Delete a sentiment by ID."""
    sentiment = db.query(SentimentData).filter(SentimentData.id == sentiment_id).first()
    if not sentiment:
        raise HTTPException(status_code=404, detail="Sentiment not found")
    db.delete(sentiment)
    db.commit()
    return {"detail": f"Sentiment with ID {sentiment_id} deleted successfully"}
