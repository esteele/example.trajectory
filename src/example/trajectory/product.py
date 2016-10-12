from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from collective.trajectory.components import Model
from example.trajectory.initializer import getSession
from example.trajectory.interfaces import IProduct
from example.trajectory.interfaces import IProductContainer
from example.trajectory.models import Product
from plone import api
import traject
from zope.interface import implements


PRODUCTS_FOLDER_ID = 'products'


def get_product_by_id(product_id):
    session = getSession()
    return session.query(Product).filter(Product.id == product_id).scalar()


def add_product(id, name="", description="", price=0.0):
    new_product = Product(id=id, name=name, description=description, price=price)
    session = getSession()
    session.add(new_product)
    session.commit()


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
        return self.product.title

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

