import datetime

from example.trajectory.interfaces import IOrder
from example.trajectory.models import Base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import types
from zope.interface import implements


class Order(Base):
    implements(IOrder)

    __tablename__ = 'orders'

    product_id = Column(
        types.Integer, ForeignKey('products.id'), primary_key=True)
    parent_id = Column(
        types.Integer, ForeignKey('customers.id'), primary_key=True)
    date = Column(types.DateTime, default=datetime.datetime.now())
