from App.class_init import InitializeClass
from example.trajectory.interfaces import IProductContainer
from example.trajectory.product.api import get_product_by_id
from example.trajectory.product.model import IProduct
from example.trajectory.trajectory import ExampleBase
from plone import api
import traject
from zope.interface import implements


PRODUCTS_FOLDER_ID = 'products'


class ProductWrapper(ExampleBase):
    """ """
    implements(IProduct)

    portal_type = 'Product'

    id = None

    def __init__(self, id):
        self.id = id
        self.product = get_product_by_id(id)

    def Title(self):
        return self.product.name

    def Description(self):
        return self.product.description


InitializeClass(ProductWrapper)


def get_wrapped_product(product):
    product_folder = api.portal.get()[PRODUCTS_FOLDER_ID]
    return ProductWrapper(product.id).__of__(product_folder)


def product_factory(id):
    if id:
        try:
            id = int(id)
        except ValueError:
            # product_folder = api.portal.get()[PRODUCTS_FOLDER_ID]
            # possible_view = product_folder.restrictedTraverse([id])
            # if possible_view:
            #     return possible_view()
            pass
        else:
            product = get_product_by_id(id)
            if product:
                return get_wrapped_product(product)
    return None


def product_arguments(obj):
    return {
        'id': obj.id,
    }


pattern = u'/:id'
traject.register(IProductContainer, pattern, product_factory)
traject.register_inverse(IProductContainer,
                         ProductWrapper, pattern, product_arguments)
