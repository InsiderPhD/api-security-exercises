from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Role(Base):
    __tablename__ = "ex12_roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)


class User(Base):
    __tablename__ = "ex12_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    display_name: Mapped[str] = mapped_column(String(100))
    role_id: Mapped[int] = mapped_column(ForeignKey("ex12_roles.id"))


