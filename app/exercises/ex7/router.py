from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.exercises.ex7 import models, schemas

router = APIRouter()


def get_current_user_uuid(x_user_uuid: str | None = Header(default=None)) -> str:
    # Simulated auth: caller sets X-User-UUID to indicate their identity
    if not x_user_uuid:
        raise HTTPException(status_code=401, detail="Missing X-User-UUID header")
    return x_user_uuid


@router.get("/", response_model=dict)
def index() -> dict:
    return {"exercise": "ex7", "description": "BOLA with users: attacker can view victim documents via user-controlled identifiers"}


@router.get("/me", response_model=schemas.User)
def whoami(current_uuid: str = Depends(get_current_user_uuid), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.uuid == current_uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/docs", response_model=list[schemas.Document])
def list_docs(current_uuid: str = Depends(get_current_user_uuid), owner: str | None = Query(default=None), db: Session = Depends(get_db)):
    # Intended: return only current user's docs
    # VULNERABILITY: if 'owner' query is provided, use it instead of the authenticated user
    target_owner = owner if owner else current_uuid
    return db.query(models.Document).filter(models.Document.owner_uuid == target_owner).all()


@router.get("/docs/{doc_id}", response_model=schemas.Document)
def get_doc(doc_id: int, current_uuid: str = Depends(get_current_user_uuid), owner: str | None = Query(default=None), db: Session = Depends(get_db)):
    # Intended: ensure the document belongs to current user
    # VULNERABILITY: allows caller to supply an arbitrary owner to bypass checks
    doc = db.query(models.Document).get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    target_owner = owner if owner else current_uuid
    if doc.owner_uuid != target_owner:
        raise HTTPException(status_code=403, detail="Forbidden for this owner")
    return doc


@router.get("/docs/all", response_model=list[schemas.Document])
def list_all_docs(_: str = Depends(get_current_user_uuid), db: Session = Depends(get_db)):
    # VULNERABILITY: exposes all documents irrespective of user
    return db.query(models.Document).order_by(models.Document.id.desc()).limit(100).all()


