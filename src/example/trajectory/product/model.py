from example.trajectory.interfaces import IProduct
from sqlalchemy import Column
from sqlalchemy import types
from zope.interface import implements
from example.trajectory.models import Base


class Product(Base):
    implements(IProduct)

    __tablename__ = 'products'

    id = Column(types.Integer, primary_key=True)
    name = Column(types.Unicode())
    description = Column(types.Unicode())
    # photo = deferred(Column(types.LargeBinary))
    price = Column(types.Float())
