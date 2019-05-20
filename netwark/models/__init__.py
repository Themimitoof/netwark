import sys
import traceback
import logging

from sqlalchemy import event
from sqlalchemy import engine_from_config, engine
from sqlalchemy.orm import scoped_session, sessionmaker, configure_mappers
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from pyramid.httpexceptions import HTTPInternalServerError
from zope.sqlalchemy import ZopeTransactionExtension

# import or define all models here to ensure they are attached to the
# Base.metadata prior to any initialization routines
from .meta import Base
from .operation import Operation, OperationResult
from .oui_vendor import OuiVendor


log = logging.getLogger(__name__)

# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()


class Database:
    databases = {}

    @classmethod
    def register(cls, name):
        if name not in cls.databases:
            cls.databases[name] = Base
        return cls.databases[name]

    @classmethod
    def get(cls, name):
        return cls.databases[name]


class SessionFactory:
    sessions = {}

    @classmethod
    def register(cls, name, scoped):
        if scoped:
            cls.sessions[name] = scoped_session(sessionmaker(
                extension=ZopeTransactionExtension()))
        else:
            cls.sessions[name] = sessionmaker()
        return cls.sessions[name]

    @classmethod
    def get(cls, name):
        return cls.sessions[name]


def create_engine(db_name, settings, prefix='sqlalchemy.', scoped=False):
    recycle_key = '%spool_recycle' % prefix
    settings = settings.copy()  # Safe modification
    settings.setdefault(recycle_key, 1800)

    ping_conf = '%sping_interval' % prefix
    ping_interval = int(settings.pop(ping_conf, 60))

    engine = engine_from_config(settings, prefix, pool_pre_ping=True)

    DBSession = SessionFactory.register(db_name, scoped)
    DBSession.configure(bind=engine)
    db = Database.register(db_name)
    db.metadata.bind = engine

    return engine


def dispose_engine(db_name):
    Database.get(db_name).metadata.bind.dispose()


def DBSession():
    return SessionFactory.get('netwark')()


def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('netwark.models')``.

    """
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    # use pyramid_tm to hook the transaction lifecycle to the request
    config.include('pyramid_tm')

    # use pyramid_retry to retry a request when transient exceptions occur
    config.include('pyramid_retry')

    # make request.dbsession available for use in Pyramid
    config.add_request_method(
        lambda r: DBSession(),
        'dbsession',
        reify=True,
    )
