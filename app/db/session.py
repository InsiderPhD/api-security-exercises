from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import SQLITE_URL


class Base(DeclarativeBase):
    pass


engine = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False},  # needed for SQLite with threads
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


