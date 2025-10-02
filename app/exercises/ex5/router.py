from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.exercises.ex5 import models, schemas

router = APIRouter()


@router.get("/", response_model=dict)
def index() -> dict:
    return {"exercise": "ex5", "description": "Order can be confirmed without payment"}


@router.post("/baskets", response_model=dict)
def create_basket(_: schemas.BasketCreate | None = None, db: Session = Depends(get_db)):
    basket = models.Basket()
    db.add(basket)
    db.commit()
    db.refresh(basket)
    return {"basket_id": basket.id}


@router.post("/baskets/{basket_id}/items", response_model=dict)
def add_item(basket_id: int, payload: schemas.ItemAdd, db: Session = Depends(get_db)):
    basket = db.query(models.Basket).get(basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")
    item = models.BasketItem(
        basket_id=basket.id,
        name=payload.name,
        unit_price_cents=payload.unit_price_cents,
        quantity=payload.quantity,
    )
    db.add(item)
    db.commit()
    return {"ok": True, "item_id": item.id}


@router.get("/baskets/{basket_id}/summary", response_model=schemas.BasketSummary)
def basket_summary(basket_id: int, db: Session = Depends(get_db)):
    basket = db.query(models.Basket).get(basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")
    items = db.query(models.BasketItem).filter(models.BasketItem.basket_id == basket.id).all()
    subtotal = sum(i.unit_price_cents * i.quantity for i in items)
    return schemas.BasketSummary(
        basket_id=basket.id,
        subtotal_cents=subtotal,
        items=[schemas.BasketItem.model_validate(i) for i in items],
    )


@router.post("/orders", response_model=schemas.OrderStatus)
def create_order(payload: schemas.OrderCreate, db: Session = Depends(get_db)):
    basket = db.query(models.Basket).get(payload.basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")
    order = models.Order(basket_id=basket.id, status="created")
    db.add(order)
    db.commit()
    db.refresh(order)
    return schemas.OrderStatus(order_id=order.id, status=order.status)


@router.post("/orders/{order_id}/confirm", response_model=schemas.OrderStatus)
def confirm_order_without_payment(order_id: int, db: Session = Depends(get_db)):
    # VULNERABILITY: No payment verification; directly moves order to 'accepted'
    order = db.query(models.Order).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = "accepted"
    db.add(order)
    db.commit()
    return schemas.OrderStatus(order_id=order.id, status=order.status)


