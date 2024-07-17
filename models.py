from db import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
    description: Mapped[str]

    prices: Mapped[List["Price"]] = relationship(back_populates="product")


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
    name: Mapped[str]


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
    price: Mapped[float]
    product_id = mapped_column(ForeignKey("products.id"))
    store_id = mapped_column(ForeignKey("stores.id"))

    product: Mapped["Product"] = relationship(back_populates="prices")
