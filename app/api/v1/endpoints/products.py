from core.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.product import Product
from schemas.product import ProductCreate
from sqlalchemy.orm import Session

product_router = APIRouter()


@product_router.get("/products")
async def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@product_router.get("/product/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        return product


@product_router.post("/product")
async def save_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(title=product.title, description=product.description)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@product_router.delete("/product/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        db.delete(product)
        db.commit()
        return {"detail": "Product deleted successfully"}
