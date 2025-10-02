from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Document(Base):
    __tablename__ = "ex6_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_uuid: Mapped[str] = mapped_column(String(36), index=True)  # pretend user id
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(String(4000))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


