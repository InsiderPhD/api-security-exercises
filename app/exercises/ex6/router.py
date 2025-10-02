from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.exercises.ex6 import models, schemas

router = APIRouter()


@router.get("/", response_model=dict)
def index() -> dict:
    return {"exercise": "ex6", "description": "BOLA: user-provided author controls access to documents"}


@router.get("/docs/{doc_id}", response_model=schemas.Document)
def get_document(doc_id: int, author: str = Query(...), db: Session = Depends(get_db)):
    # VULNERABILITY: authorization is based solely on user-supplied author UUID matching the document
    doc = db.query(models.Document).get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.author_uuid != author:
        raise HTTPException(status_code=403, detail="Forbidden for this author")
    return doc


@router.get("/docs", response_model=list[schemas.Document])
def list_documents(author: str = Query(...), db: Session = Depends(get_db)):
    # VULNERABILITY: relies on user-supplied author to scope results; attacker can enumerate others
    return db.query(models.Document).filter(models.Document.author_uuid == author).all()


@router.get("/docs/all", response_model=list[schemas.Document])
def list_all_documents(db: Session = Depends(get_db)):
    # VULNERABILITY: endpoint exposes all documents regardless of author
    return db.query(models.Document).order_by(models.Document.id.desc()).limit(100).all()


