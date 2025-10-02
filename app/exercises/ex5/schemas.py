from pydantic import BaseModel


class BasketCreate(BaseModel):
    pass


class ItemAdd(BaseModel):
    name: str
    unit_price_cents: int
    quantity: int = 1


class OrderCreate(BaseModel):
    basket_id: int


class BasketItem(BaseModel):
    id: int
    name: str
    unit_price_cents: int
    quantity: int

    class Config:
        from_attributes = True


class BasketSummary(BaseModel):
    basket_id: int
    subtotal_cents: int
    items: list[BasketItem]


class OrderStatus(BaseModel):
    order_id: int
    status: str


