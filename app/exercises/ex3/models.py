from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Coupon(Base):
    __tablename__ = "ex3_coupons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    discount_amount_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    remaining_uses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class Basket(Base):
    __tablename__ = "ex3_baskets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    items: Mapped[list["BasketItem"]] = relationship(
        "app.exercises.ex3.models.BasketItem",
        back_populates="basket",
        cascade="all, delete-orphan",
    )
    coupon_applications: Mapped[list["BasketCouponApplication"]] = relationship(
        "app.exercises.ex3.models.BasketCouponApplication",
        back_populates="basket",
        cascade="all, delete-orphan",
    )


class BasketItem(Base):
    __tablename__ = "ex3_basket_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    basket_id: Mapped[int] = mapped_column(ForeignKey("ex3_baskets.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(128))
    unit_price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    basket: Mapped[Basket] = relationship(
        "app.exercises.ex3.models.Basket",
        back_populates="items",
    )


class BasketCouponApplication(Base):
    __tablename__ = "ex3_basket_coupon_applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    basket_id: Mapped[int] = mapped_column(ForeignKey("ex3_baskets.id", ondelete="CASCADE"))
    coupon_id: Mapped[int] = mapped_column(ForeignKey("ex3_coupons.id", ondelete="RESTRICT"))

    basket: Mapped[Basket] = relationship(
        "app.exercises.ex3.models.Basket",
        back_populates="coupon_applications",
    )
    coupon: Mapped[Coupon] = relationship("app.exercises.ex3.models.Coupon")

