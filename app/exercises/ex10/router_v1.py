from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.exercises.ex10 import models, schemas

router = APIRouter()


@router.get("/products", response_model=list[schemas.Product])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).order_by(models.Product.id.asc()).all()


@router.post("/purchase", response_model=dict)
def purchase(payload: schemas.Purchase, db: Session = Depends(get_db)):
    # VULNERABILITY: No inventory check; stock can go negative
    product = db.query(models.Product).get(payload.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.stock -= payload.quantity
    db.add(product)
    db.commit()
    return {"ok": True, "product_id": product.id, "remaining_stock": product.stock}


