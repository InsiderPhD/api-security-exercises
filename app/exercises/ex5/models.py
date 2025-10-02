from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Basket(Base):
    __tablename__ = "ex5_baskets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    items: Mapped[list["BasketItem"]] = relationship(
        "app.exercises.ex5.models.BasketItem",
        back_populates="basket",
        cascade="all, delete-orphan",
    )


class BasketItem(Base):
    __tablename__ = "ex5_basket_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    basket_id: Mapped[int] = mapped_column(ForeignKey("ex5_baskets.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(128))
    unit_price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    basket: Mapped[Basket] = relationship(
        "app.exercises.ex5.models.Basket",
        back_populates="items",
    )


class Order(Base):
    __tablename__ = "ex5_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    basket_id: Mapped[int] = mapped_column(ForeignKey("ex5_baskets.id", ondelete="RESTRICT"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(32), default="created")

