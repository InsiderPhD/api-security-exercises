from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.exercises.ex8 import models, schemas

router = APIRouter()


@router.get("/", response_model=dict)
def index() -> dict:
    return {"exercise": "ex8", "description": "Sensitive data exposure in API responses"}


@router.get("/customers/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    # VULNERABILITY: returns full customer record including sensitive fields
    cust = db.query(models.Customer).get(customer_id)
    if not cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    return cust


@router.get("/customers", response_model=list[schemas.Customer])
def list_customers(db: Session = Depends(get_db)):
    # VULNERABILITY: bulk endpoint leaking sensitive fields for all customers
    return db.query(models.Customer).order_by(models.Customer.id.asc()).limit(50).all()


