# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from example.trajectory import _
from zope import schema
from zope.interface import Attribute
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IDatabaseLoginOptions(Interface):
    """ Interface for database logins """
    dsn = Attribute("DSN string to connect to a database")


class IExampleTrajectoryLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IProductContainer(Interface):
    """ """


class IProduct(Interface):
    """ """


class ICustomer(Interface):
    """ """


class IOrder(Interface):
    """ """
