from pydantic import BaseModel


class ProductBase(BaseModel):
    title: str
    description: str | None = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
