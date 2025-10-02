from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Message(Base):
    __tablename__ = "ex1_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(String(500), nullable=False)


