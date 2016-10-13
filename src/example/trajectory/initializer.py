import logging
import os
import uuid
from threading import RLock
from threading import local

from ZPublisher.interfaces import IPubFailure
from ZPublisher.interfaces import IPubStart
from ZPublisher.interfaces import IPubSuccess
from example.trajectory.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from zope.component import adapter
from zope.component import getGlobalSiteManager
from zope.component import provideHandler
from zope.interface import implements
from example.trajectory.interfaces import IDatabaseLoginOptions


# quickly turn on datbase debugging
DEBUG = False

# configure logging through python logger insteda of the default
# sqlalchemy who knows logger
logging.basicConfig()

if DEBUG:
    # We don't need this for day to day but leaving it here for quick access
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)

_DB_CONFIG_LOCK = RLock()

_PROFILE_SESSION = None
_PROFILE_ENGINE = None
_SQLA = local()


def _create_database_if_missing(dsn):
    from copy import copy
    from sqlalchemy.engine.url import make_url
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    url = copy(make_url(dsn))
    database = url.database
    url.database = 'template1'
    engine = create_engine(url)
    query = "SELECT 1 FROM pg_database WHERE datname='%s'" % database
    exists = bool(engine.execute(query).scalar())
    if not exists:
        engine.raw_connection().set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        query = "CREATE DATABASE {0} ENCODING '{1}' TEMPLATE {2}".format(
            database,
            'utf8',
            'template0'
        )
        engine.execute(query)



def getProfileSession():
    if not _PROFILE_SESSION:
        initializeSqlIntegration()
    return _PROFILE_SESSION


def getProfileEngine():
    if not _PROFILE_ENGINE:
        initializeSqlIntegration()
    return _PROFILE_ENGINE


def initializeSqlIntegration():
    gsm = getGlobalSiteManager()
    dbconfig = gsm.queryUtility(IDatabaseLoginOptions)
    if not dbconfig:
        raise Exception("Could not lookup database dsn. Please check configuration")

    '''
    since we moved this code out of the actual init, so that we can have
    a sane configuration setup, we MUST do this with a lock. Otherwise sql
    alchemy loses its shit and goes on a 'fuck you muli-threading - I'll eat
    pancakes on your grave!' tirade. Then you spend your friday
    night sober and staring at an abyss of configuration headaches and
    infinite loops usually reserved for Mondays.
    '''

    with _DB_CONFIG_LOCK:
        global _PROFILE_ENGINE
        global _PROFILE_SESSION
        global DEBUG

        if not _PROFILE_ENGINE:
            _create_database_if_missing(dbconfig.dsn)
            _PROFILE_ENGINE = create_engine(dbconfig.dsn,
                                            pool_size=5,
                                            pool_recycle=3600,
                                            convert_unicode=True,
                                            echo=DEBUG,
                                            )
            Base.metadata.create_all(_PROFILE_ENGINE)

        if not _PROFILE_SESSION:
            _PROFILE_SESSION = scoped_session(sessionmaker(bind=_PROFILE_ENGINE))


def initializeSession():
    """
    Create a session local to a thread. Historically this was on
    the request object. Turns out this was a terrible idea since
    plone has a gabillion requests per request, and there is no
    guaruntee that one can get the request from certain threads.

    Also note that for some reason, in 4.2, this access is happening
    from the dummy startup thread, and not the main thread. I have no
    idea how this will affect things long term.
    """
    _SQLA.session = getProfileSession()


def getSession():
    """
    """
    # XXX: we can check for errors and what not here later
    # e.g. if a transaction needs rolled back or something
    if not getattr(_SQLA, 'session', None):
        initializeSession()
    return _SQLA.session


def closeSession():
    session = getSession()
    if session:
        session.close()


@adapter(IPubStart)
def configureSessionOnStart(event):
    initializeSession()


@adapter(IPubSuccess)
def persistSessionOnSuccess(event):
    closeSession()


@adapter(IPubFailure)
def persistSessionOnFailure(event):
    if not event.retry:
        closeSession()


# setup and tear down sessions in the request object
provideHandler(configureSessionOnStart)
provideHandler(persistSessionOnSuccess)
provideHandler(persistSessionOnFailure)


class TestDatabaseLogin(object):
    implements(IDatabaseLoginOptions)
    dsn = "postgresql://example:example!@localhost/exampledb_testing"


class LocalDatabaseLogin(object):
    implements(IDatabaseLoginOptions)
    dsn = "postgresql://example:example!@localhost/exampledb"
