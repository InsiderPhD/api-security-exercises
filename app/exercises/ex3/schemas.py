from pydantic import BaseModel


class BasketCreate(BaseModel):
    pass


class ItemAdd(BaseModel):
    name: str
    unit_price_cents: int
    quantity: int = 1


class ApplyCoupon(BaseModel):
    code: str


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
    discount_cents: int
    total_cents: int
    items: list[BasketItem]


