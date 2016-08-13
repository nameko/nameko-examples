import datetime

from sqlalchemy import (
    DECIMAL, Column, DateTime, ForeignKey, Integer,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Base(object):
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )
    deleted_at = Column(DateTime, nullable=True)

    def delete(self):
        if self.deleted_at is None:
            self.deleted_at = datetime.datetime.utcnow()


Base = declarative_base(cls=Base)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)


class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True)
    order_id = Column(
        Integer,
        ForeignKey("orders.id", name="fk_order_details_orders"),
        nullable=False
    )
    order = relationship(Order, backref="order_details")
    product_id = Column(Integer, nullable=False)
    price = Column(DECIMAL(18, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
