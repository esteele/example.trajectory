from Acquisition import aq_base
from Acquisition import aq_get
from example.trajectory import _
from example.trajectory.db import getSession
from example.trajectory.product.model import IProduct
from example.trajectory.product.model import Product
from example.trajectory.product.trajectory import get_wrapped_product
from plone.app.contentlisting.contentlisting import BaseContentListingObject
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.app.z3cform.layout import FormWrapper
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import schema
from zope.interface import implementer
from zope.publisher.browser import BrowserView


class AddForm(form.AddForm):
    fields = field.Fields(IProduct)

    def create(self, data):
        from example.trajectory.product.api import add_product
        return add_product(**data)

    def add(self, object):
        from example.trajectory.product.trajectory import product_factory
        self.wrapper = product_factory(object.id)

    def nextURL(self):
        return self.wrapper.absolute_url()


class AddView(FormWrapper):
    form = AddForm


class EditForm(form.EditForm):
    fields = field.Fields(IProduct)

    def getContent(self):
        product = self.context.product
        ret = {'id': product.id}
        for field_id in schema.getFields(IProduct):
            ret[field_id] = getattr(product, field_id)
        return ret

    def applyChanges(self, data):
        content = self.getContent()
        changes = form.applyChanges(self, content, data)
        if changes:
            product = self.context.product
            for changed_field in changes[IProduct]:
                new_value = data[changed_field]
                setattr(product, changed_field, new_value)
            session = getSession()
            session.add(product)
            session.commit()
        return bool(changes)

    @button.buttonAndHandler(_('Apply'), name='apply')
    def handleApply(self, action):
        super(EditForm, self).handleApply(self, action)
        # Return to default view of the object,
        # since form.EditForm doesn't do nextURL.
        self.request.response.redirect(self.context.absolute_url())


class EditView(FormWrapper):
    form = EditForm


class View(BrowserView):
    """ """


class ContentListing(BrowserView):
    def __call__(self, batch=False, b_size=20, b_start=0, orphan=0, **kw):
        results = getSession().query(Product).all()
        return IContentListing(results)[b_start:b_size]


@implementer(IContentListingObject)
class ProductListing(BaseContentListingObject):
    """ """
    def __init__(self, obj):
        self._object = obj
        self._wrapped = get_wrapped_product(obj)

    def __getattr__(self, name):
        """We'll override getattr so that we can defer name lookups to the real
        underlying objects without knowing the names of all attributes.
        """
        if name.startswith('_'):
            raise AttributeError(name)
        if hasattr(aq_base(self._object), name):
            return getattr(self._object, name)
        if hasattr(aq_base(self._wrapped), name):
            return getattr(self._wrapped, name)
        else:
            # Otherwise, we really don't care.
            return None
            # raise AttributeError(name)

    def PortalType(self):
        return self.portal_type

    def getId(self):
        return self._object.id

    def getURL(self):
        return self._wrapped.absolute_url()
