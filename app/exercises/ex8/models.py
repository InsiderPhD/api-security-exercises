from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Customer(Base):
    __tablename__ = "ex8_customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200))
    # Sensitive fields that should not be returned
    ssn: Mapped[str] = mapped_column(String(20))
    credit_card_number: Mapped[str] = mapped_column(String(32))
    api_key: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


