from example.trajectory import _
from example.trajectory.models import Base
from plone.supermodel import model
from sqlalchemy import Column
from sqlalchemy import types
from zope import schema
from zope.interface import implements
from plone.dexterity.browser import edit
from zope.publisher.browser import BrowserView


class IProduct(model.Schema):
    """ """

    name = schema.TextLine(title=_(u'Name'), required=True)
    description = schema.Text(title=_(u'Description'), required=False)
    price = schema.Float(title=_(u'Price'), required=False)


class Product(Base):
    implements(IProduct)

    __tablename__ = 'products'

    id = Column(types.Integer, primary_key=True)
    name = Column(types.Unicode())
    description = Column(types.Unicode())
    # photo = deferred(Column(types.LargeBinary))
    price = Column(types.Float())



class EditForm(edit.DefaultEditForm):
    pass


class View(BrowserView):
    """ """


class ProductListingView(BrowserView):
    """ """

