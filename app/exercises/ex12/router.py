from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.exercises.ex12 import models, schemas

router = APIRouter()


def get_current_user(db: Session, user_email_header: str | None) -> models.User:
    if not user_email_header:
        raise HTTPException(status_code=401, detail="Missing X-User-Email header")
    user = db.query(models.User).filter(models.User.email == user_email_header).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=dict)
def index() -> dict:
    return {"exercise": "ex12", "description": "Mass assignment: user can set role_id to escalate privileges"}


@router.get("/me", response_model=schemas.User)
def me(x_user_email: str | None = Header(default=None, alias="X-User-Email"), db: Session = Depends(get_db)):
    user = get_current_user(db, x_user_email)
    return user


@router.patch("/me", response_model=schemas.User)
def update_me(
    payload: schemas.UserUpdate,
    x_user_email: str | None = Header(default=None, alias="X-User-Email"),
    db: Session = Depends(get_db),
):
    user = get_current_user(db, x_user_email)

    # VULNERABILITY: mass assignment - apply all provided fields directly onto the user, including role_id
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


