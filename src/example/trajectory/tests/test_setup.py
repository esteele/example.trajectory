# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from example.trajectory.testing import EXAMPLE_TRAJECTORY_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that example.trajectory is properly installed."""

    layer = EXAMPLE_TRAJECTORY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if example.trajectory is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'example.trajectory'))

    def test_product_folder_created(self):
        """Test that /products is created."""
        from example.trajectory.interfaces import IProductContainer
        from example.trajectory.product import PRODUCTS_FOLDER_ID
        self.assertIn(PRODUCTS_FOLDER_ID, self.portal.objectIds())
        self.assertTrue(IProductContainer.providedBy(self.portal[PRODUCTS_FOLDER_ID]))


class TestUninstall(unittest.TestCase):

    layer = EXAMPLE_TRAJECTORY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['example.trajectory'])

    def test_product_uninstalled(self):
        """Test if example.trajectory is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'example.trajectory'))

    def test_browserlayer_removed(self):
        """Test that IExampleTrajectoryLayer is removed."""
        from example.trajectory.interfaces import IExampleTrajectoryLayer
        from plone.browserlayer import utils
        self.assertNotIn(IExampleTrajectoryLayer, utils.registered_layers())
