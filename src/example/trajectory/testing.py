# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from sqlalchemy import event
from sqlalchemy.exc import OperationalError
from sqlalchemy.schema import MetaData

import example.trajectory
from example.trajectory.db import getSession


class ExampleTrajectoryLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=example.trajectory)
        self.loadZCML(package=example.trajectory, name='configure-test.zcml')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'example.trajectory:default')

    def testSetUp(self):
        super(ExampleTrajectoryLayer, self).testSetUp()

        # Begin a nested transaction, that we can roll back after each test,
        # and start the next with a clean database.
        self['session'] = getSession()
        self['session'].begin_nested()

        @event.listens_for(self['session'], 'after_transaction_end')
        def restart_savepoint(session, transaction):
            if transaction.nested and not transaction._parent.nested:
                session.expire_all()
                session.begin_nested()

    def testTearDown(self):
        super(ExampleTrajectoryLayer, self).testTearDown()
        # self['session'].expire_all()
        self['session'].close()


EXAMPLE_TRAJECTORY_FIXTURE = ExampleTrajectoryLayer()


EXAMPLE_TRAJECTORY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EXAMPLE_TRAJECTORY_FIXTURE,),
    name='ExampleTrajectoryLayer:IntegrationTesting'
)


EXAMPLE_TRAJECTORY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EXAMPLE_TRAJECTORY_FIXTURE,),
    name='ExampleTrajectoryLayer:FunctionalTesting'
)
