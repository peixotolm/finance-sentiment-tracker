from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.stock import StockData
from app.models.product import Product
from app.schemas.stock import StockCreate

stock_router = APIRouter()


@stock_router.get("/stocks")
async def list_stocks(db: Session = Depends(get_db)):
    """Retrieve all stock records."""
    return db.query(StockData).all()


@stock_router.get("/stock/{stock_id}")
async def get_stock(stock_id: int, db: Session = Depends(get_db)):
    """Retrieve stock data by ID."""
    stock = db.query(StockData).filter(StockData.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock data not found")
    return stock


@stock_router.post("/stocks")
async def save_stock(stock: StockCreate, db: Session = Depends(get_db)):
    """Create a new stock record."""
    # Check if the product exists
    product = db.query(Product).filter(Product.title == stock.product_name).first()
    if not product:
        raise HTTPException(
            status_code=400,
            detail=f"Product with name '{stock.product_name}' does not exist.",
        )

    # Create the StockData entry
    new_stock = StockData(
        product_name=stock.product_name,
        price=stock.price,
        open_price=stock.open_price,
        close_price=stock.close_price,
        high=stock.high,
        low=stock.low,
        volume=stock.volume,
        date=stock.date,
    )
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return new_stock


@stock_router.delete("/stock/{stock_id}")
async def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    """Delete a stock record by ID."""
    stock = db.query(StockData).get(stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock data not found")
    db.delete(stock)
    db.commit()
    return {"detail": f"Stock data with ID {stock_id} deleted successfully"}
