import logging
import os
from threading import RLock
from threading import local

from ZPublisher.interfaces import IPubStart
from ZPublisher.interfaces import IPubStartIPubFailure
from ZPublisher.interfaces import IPubStartIPubSuccess
from example.trajectory.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from zope.component import adapter
from zope.component import provideHandler


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


DSN = "postgresql://postgres:example!@localhost/exampledb"


'''
We need to:
  1. delay config until first request so that we can use a utility to
     direct which connection we are
  2. encapsulate access to these globals
This shouldn't be in __init__ long term - leaving it here for backwards
compat aka pure laziness.
'''


def getProfileSession():
    if not _PROFILE_SESSION:
        initializeSqlIntegration()
    return _PROFILE_SESSION


def getProfileEngine():
    if not _PROFILE_ENGINE:
        initializeSqlIntegration()
    return _PROFILE_ENGINE


# def _create_database_if_missing(dsn):
#     from copy import copy
#     from sqlalchemy.engine.url import make_url
#     from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
#     url = copy(make_url(dsn))
#     database = url.database
#     url.database = 'template1'
#     engine = create_engine(url)
#     query = "SELECT 1 FROM pg_database WHERE datname='%s'" % database
#     exists = bool(engine.execute(query).scalar())
#     if not exists:
#         engine.raw_connection().set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#         query = "CREATE DATABASE {0} ENCODING '{1}' TEMPLATE {2}".format(
#             database,
#             'utf8',
#             'template0'
#         )
#         engine.execute(query)


def initializeSqlIntegration():
    '''
    since we moved this code out of the actual init, so that we can have
    a sane configuration setup, we MUST do this with a lock. Otherwise sql
    alchemy loses its shit and goes on a 'fuck you muli-threading - I'll eat
    pancakes on your grave!' tirade. Then you spend your friday
    night sober and staring at an abyss of configuration headaches and
    infinite loops usually reserved for Mondays.
    '''

    # Enforce UTC as our base timezone.
    os.putenv( "PGTZ", "UTC" )

    with _DB_CONFIG_LOCK:
        global _PROFILE_ENGINE
        global _PROFILE_SESSION
        global DEBUG

        if not _PROFILE_ENGINE:
            # _create_database_if_missing(DSN)
            _PROFILE_ENGINE = create_engine(DSN,
                                            pool_size=5,
                                            pool_recycle=3600,
                                            convert_unicode=True,
                                            echo=DEBUG,
                                            )
            # The amp profile MUST be initialized before all the
            # rest, whih is why we don't have a utility for it
            Base.metadata.create_all(_PROFILE_ENGINE)
            # we actually need to do this with all of the
            # classes which provide this so that everything works
            # all dandy.
            # initializers = zope.component.getUtilitiesFor(IAmpDatabaseConfiguration)
            # for name, initializer in initializers:
            #     initializer.initialize(_PROFILE_ENGINE)

        if not _PROFILE_SESSION:
            '''
            expire_on_commit is set to false at the moment because
            we are using an in memory cache. I don't think that long
            term this is a good decision although I'm having issues
            finding good information on it.If things get funcky, set
            this to True and change the beaker cache to something
            that requires pickles like memcached or disk
            '''
            _PROFILE_SESSION = scoped_session(sessionmaker(bind=_PROFILE_ENGINE,
                                                           expire_on_commit=False,))


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
    session = getSession(request)
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