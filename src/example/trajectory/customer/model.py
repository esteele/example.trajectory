from example.trajeectory.models import Base
from example.trajectory.interfaces import ICustomer
from sqlalchemy import Column
from sqlalchemy import types
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import synonym
from zope.interface import implements


class Customer(Base):
    implements(ICustomer)

    __tablename__ = 'customers'

    id = Column(types.Integer, primary_key=True)
    _firstname = Column("firstname", types.Unicode)
    _lastname = Column("lastname", types.Unicode)
    _fullname = Column("fullname", types.Unicode)

    email = Column(types.Unicode)
    address = Column(types.Unicode(convert_unicode="force",))

    # We don't want fullname to be settable
    # However, we do want to allow plone to query on fullname,
    # so we are going to store it in the data.
    def get_fullname(self):
        return self._fullname

    def set_fullname(self, value):
        self._fullname = self.getFullName()

    @declared_attr
    def fullname(cls):
        return synonym('_fullname', descriptor=property(cls.get_fullname, cls.set_fullname))

    # We want fullname to be reset whenever first, or last
    # are changed.
    def get_firstname(self):
        return self._firstname

    def set_firstname(self, value):
        self._firstname = value
        self.fullname = self.getFullName()

    @declared_attr
    def firstname(cls):
        return synonym('_firstname', descriptor=property(cls.get_firstname, cls.set_firstname))

    def get_lastname(self):
        return self._lastname

    def set_lastname(self, value):
        self._lastname = value
        self.fullname = self.getFullName()

    @declared_attr
    def lastname(cls):
        return synonym('_lastname', descriptor=property(cls.get_lastname, cls.set_lastname))

    def getFullName(self):
        """
        Returns the user's first and last name. If those are empty, return
        the user id for display purposes.
        """
        if self.firstname or self.lastname:
            return "%s %s" % (self.firstname, self.lastname)
        return self.plone_id

    def getSortableName(self):
        """ Return the user's name in lastname firstname format so that
            for sorting purposes.
        """
        return "%s %s" % (self.lastname, self.firstname)
