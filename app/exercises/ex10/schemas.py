from pydantic import BaseModel


class Purchase(BaseModel):
    product_id: int
    quantity: int


class Product(BaseModel):
    id: int
    name: str
    price_cents: int
    stock: int

    class Config:
        from_attributes = True


