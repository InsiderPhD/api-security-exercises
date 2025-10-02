from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.exercises.ex3 import models, schemas

router = APIRouter()


@router.get("/", response_model=dict)
def index() -> dict:
    return {"exercise": "ex3", "description": "Unrestricted coupon stacking on a single basket"}


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


@router.post("/baskets/{basket_id}/apply-coupon", response_model=dict)
def apply_coupon(basket_id: int, payload: schemas.ApplyCoupon, db: Session = Depends(get_db)):
    basket = db.query(models.Basket).get(basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")

    coupon = db.query(models.Coupon).filter(models.Coupon.code == payload.code).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")

    # VULNERABILITY: Allow stacking coupon multiple times on same basket without decrementing remaining_uses per basket usage
    if coupon.remaining_uses <= 0:
        raise HTTPException(status_code=400, detail="Coupon exhausted")

    application = models.BasketCouponApplication(basket_id=basket.id, coupon_id=coupon.id)
    db.add(application)

    # Incorrectly decrement global remaining_uses by 1 regardless of per-basket stacking
    coupon.remaining_uses -= 1

    db.commit()
    return {"ok": True, "applied": payload.code, "remaining_uses": coupon.remaining_uses}


@router.get("/baskets/{basket_id}/summary", response_model=schemas.BasketSummary)
def basket_summary(basket_id: int, db: Session = Depends(get_db)):
    basket = db.query(models.Basket).get(basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")

    items = db.query(models.BasketItem).filter(models.BasketItem.basket_id == basket.id).all()
    subtotal = sum(i.unit_price_cents * i.quantity for i in items)

    # Vulnerable calculation: apply discount for each application of the same coupon
    applications = db.query(models.BasketCouponApplication).filter(
        models.BasketCouponApplication.basket_id == basket.id
    ).all()
    discount = 0
    for app in applications:
        coupon = db.query(models.Coupon).get(app.coupon_id)
        if coupon:
            discount += coupon.discount_amount_cents

    total = max(subtotal - discount, 0)

    return schemas.BasketSummary(
        basket_id=basket.id,
        subtotal_cents=subtotal,
        discount_cents=discount,
        total_cents=total,
        items=[schemas.BasketItem.model_validate(i) for i in items],
    )


