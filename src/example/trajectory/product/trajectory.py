from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from collective.trajectory.components import Model
from example.trajectory.product.model import IProduct
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
        return "<%s %s>" % (self.__class__.__name__, self.id)

    def __getitem__(self, name):
        traverse = self.restrictedTraverse(name)
        return traverse

    def __contains__(self, name):
        return False

    def Title(self):
        return self.product.name

    def Description(self):
        return self.product.description


InitializeClass(ProductWrapper)

def product_factory(id):
    if id:
        portal = api.portal.get()
        product_folder = portal[PRODUCTS_FOLDER_ID]
        try:
            id = int(id)
        except ValueError:
            # possible_view = product_folder.restrictedTraverse([id])
            # import pdb; pdb.set_trace( )
            # if possible_view:
            #     return possible_view()
            pass
        else:
            product = get_product_by_id(id)
            if product:
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

from plone.app.contentlisting.contentlisting import BaseContentListingObject
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.app.contentlisting.interfaces import IContentListing
from zope.interface import implementer
from Acquisition import aq_base
from Acquisition import aq_get
from example.trajectory.db import getSession
from example.trajectory.product.model import Product
from zope.publisher.browser import BrowserView


class ContentListing(BrowserView):
    def __call__(self, batch=False, b_size=20, b_start=0, orphan=0, **kw):
        results = getSession().query(Product).all()
        return IContentListing(results)


@implementer(IContentListingObject)
class ProductListing(BaseContentListingObject):
    """ """
    def __init__(self, obj):
        self._object = obj

    def __getattr__(self, name):
        """We'll override getattr so that we can defer name lookups to the real
        underlying objects without knowing the names of all attributes.
        """

        if name.startswith('_'):
            raise AttributeError(name)
        if hasattr(aq_base(self._object), name):
            return getattr(self._object, name)
        else:
            raise AttributeError(name)
