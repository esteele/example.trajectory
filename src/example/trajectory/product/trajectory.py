from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from collective.trajectory.components import Model
from example.trajectory.interfaces import IProduct
from example.trajectory.interfaces import IProductContainer
from plone import api
import traject
from zope.interface import implements
from .api import get_product_by_id


PRODUCTS_FOLDER_ID = 'products'


class ProductWrapper(Model):
    """ """
    implements(IProduct)
    security = ClassSecurityInfo()

    id = None

    def __init__(self, id):
        self.id = id
        self.product = get_product_by_id(id)

    def __repr__(self):
        return "%s(for product %s)" % (self.__class__, self.id)

    def Title(self):
        return self.product.name

InitializeClass(ProductWrapper)


def product_factory(id):
    if id:
        product = get_product_by_id(id)
        if product:
            portal = api.portal.get()
            product_folder = portal[PRODUCTS_FOLDER_ID]
            return ProductWrapper(id).__of__(product_folder)
    return None


def product_arguments(obj):
    return {
        'id': obj.id,
    }


pattern = u'/:id'
traject.register(IProductContainer, pattern, product_factory)
traject.register_inverse(IProductContainer,
                         ProductWrapper, pattern, product_arguments)
