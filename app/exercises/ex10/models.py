from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Product(Base):
    __tablename__ = "ex10_products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    price_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


