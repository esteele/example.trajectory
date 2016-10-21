# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from example.trajectory.testing import EXAMPLE_TRAJECTORY_INTEGRATION_TESTING  # noqa
from example.trajectory.product.model import Product
from example.trajectory.db import getSession
from plone import api

import unittest


class TestOrder(unittest.TestCase):

    layer = EXAMPLE_TRAJECTORY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_order_creation(self):
        """Test that add_product call creates products is created."""
        from example.trajectory.order.model import Order
        from example.trajectory.order.model import OrderItem
        from example.trajectory.db import getSession
        from example.trajectory.customer.api import add_customer
        from example.trajectory.customer.model import Customer
        from example.trajectory.product.api import add_product
        from example.trajectory.product.model import Product
        session = getSession()

        bfergler = add_customer(
            firstname='Bert', lastname='Fergler', email='bfergler@example.com')
        rnyan = add_customer(
            firstname='Ryan', lastname='Nyan', email='rrnyam@example.com')
        jlocker = add_customer(
            firstname='Jim', lastname='Locker', email='jlocker@example.com')

        product_1 = add_product(name='Widget Wash', price=9.75)
        product_2 = add_product(name='Content Bucket', price=19.99)

        order = Order(customer=bfergler)
        session.add(order)
        session.commit()

        item = OrderItem(order=order, product=product_1, quantity=5)
        session.add(item)
        item2 = OrderItem(order=order, product=product_2, quantity=2)
        session.add(item2)
        session.commit()


        import pdb; pdb.set_trace( )


