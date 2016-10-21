from example.trajectory.models import Base
from example.trajectory.customer.model import Customer
from example.trajectory.product.model import Product
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import types
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

from example.trajectory.db import UTCDateTime
from example.trajectory.db import utcnow


class Order(Base):
    __tablename__ = 'orders'

    id = Column(types.Integer, primary_key=True)
    customer_id = Column(
        types.Integer, ForeignKey('customers.id'))
    date = Column(UTCDateTime, default=utcnow())

    customer = relationship('Customer',
                            backref=backref('orders', lazy='dynamic'),
                            primaryjoin=customer_id == Customer.id)


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(types.Integer, primary_key=True)
    order_id = Column(types.Integer, ForeignKey('orders.id'))
    product_id = Column(types.Integer, ForeignKey('products.id'))

    quantity = Column(types.Integer)

    product = relationship('Product',
                           primaryjoin=product_id == Product.id)

    order = relationship('Order',
                         primaryjoin=order_id == Order.id,
                         backref=backref('items', lazy='dynamic'))
