# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api
from zope.interface import alsoProvides
from example.trajectory.interfaces import IProductContainer
from example.trajectory.product.trajectory import PRODUCTS_FOLDER_ID


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'example.trajectory:uninstall',
        ]


def add_product_folder(portal):
    folder_id = PRODUCTS_FOLDER_ID
    folder_title = 'Products'
    products_folder = portal.get(folder_id)
    if not products_folder:
        products_folder = api.content.create(id=folder_id,
                                             title=folder_title,
                                             type="Folder",
                                             container=portal,
                                             safe_id=False)
        api.content.transition(obj=products_folder, transition="publish")
    alsoProvides(products_folder, IProductContainer)
    products_folder.setLayout('@@listing_view')


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    portal = api.portal.get()
    add_product_folder(portal)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
