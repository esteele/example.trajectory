from AccessControl import ClassSecurityInfo
from collective.trajectory.components import Model
from Products.CMFCore.DynamicType import DynamicType


class ExampleBase(Model, DynamicType):
    security = ClassSecurityInfo()

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.id)

    def __getitem__(self, name):
        traverse = self.restrictedTraverse(name)
        return traverse

    def __contains__(self, name):
        return False
