from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.exercises.ex1 import schemas, models

router = APIRouter()


@router.get("/", response_model=dict)
def index() -> dict:
    return {"exercise": "ex1", "description": "Intro endpoints with SQLite, try looking at the message endpoint"}


@router.post("/messages", response_model=schemas.Message)
def create_message(payload: schemas.MessageCreate, db: Session = Depends(get_db)):
    message = models.Message(content=payload.content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@router.get("/messages", response_model=list[schemas.Message])
def list_messages(db: Session = Depends(get_db)):
    return db.query(models.Message).all()


@router.get("/messages/{message_id}", response_model=schemas.Message)
def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(models.Message).get(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


