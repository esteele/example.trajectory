# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from example.trajectory.testing import EXAMPLE_TRAJECTORY_INTEGRATION_TESTING  # noqa
from example.trajectory.product.model import Product
from example.trajectory.db import getSession
from plone import api

import unittest


class TestProduct(unittest.TestCase):
    """Test that example.trajectory is properly installed."""

    layer = EXAMPLE_TRAJECTORY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_product_creation(self):
        """Test that add_product call creates products is created."""
        from example.trajectory.product.api import add_product
        product = add_product(name='Widget Wash', price=9.75)
        self.assertEqual(getSession().query(Product).count(), 1)

