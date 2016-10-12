# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import example.trajectory


class ExampleTrajectoryLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=example.trajectory)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'example.trajectory:default')


EXAMPLE_TRAJECTORY_FIXTURE = ExampleTrajectoryLayer()


EXAMPLE_TRAJECTORY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EXAMPLE_TRAJECTORY_FIXTURE,),
    name='ExampleTrajectoryLayer:IntegrationTesting'
)


EXAMPLE_TRAJECTORY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EXAMPLE_TRAJECTORY_FIXTURE,),
    name='ExampleTrajectoryLayer:FunctionalTesting'
)
