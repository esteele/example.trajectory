# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from example.trajectory.testing import EXAMPLE_TRAJECTORY_INTEGRATION_TESTING  # noqa
from example.trajectory.db import getSession
from example.trajectory.customer.api import add_customer
from example.trajectory.customer.model import Customer
from plone import api


import unittest


class TestCustomer(unittest.TestCase):

    layer = EXAMPLE_TRAJECTORY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_customer_creation(self):
        """Test that add_customer call creates customers"""
        customer = add_customer(firstname='Bert', lastname='Fergler')
        self.assertEqual(getSession().query(Customer).count(), 1)
        self.assertEqual(customer.firstname, u'Bert')
        self.assertEqual(customer.lastname, u'Fergler')
        self.assertEqual(customer.fullname, u'Bert Fergler')
