import logging

from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pyramid.events import NewRequest
from celery import Celery

from .events import flash_messages
from .backend import configure_celery
from .models import create_engine
from .models.operation import OPERATION_FLAGS

log = logging.getLogger(__name__)
celery_app = Celery(include=['netwark.backend.tasks'])

__VERSION__ = '0.1.0'


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        log.debug('Importing modules and routes...')
        config.include('cornice')
        config.include('.models')
        config.include('pypugjs.ext.pyramid')
        config.include('.geoip')
        config.include('.routes')
        config.include('.api.v1')

        # Configure SQLAlchemy session
        create_engine('netwark', settings, scoped=True)

        # Configure session factory
        log.debug('Configuring the session factory...')
        session_factory = SignedCookieSessionFactory(
            config.registry.settings['session.token']
        )
        config.set_session_factory(session_factory)

        # Add operation glags to request methods
        def operation_flags(request):
            return OPERATION_FLAGS

        config.add_request_method(
            operation_flags, 'operation_flags', reify=True
        )

        # Execute flash_messages method when a new request happen
        config.add_subscriber(flash_messages, NewRequest)

        log.debug('Scanning views and errors modules...')
        config.scan('.views')
        config.scan('netwark.helpers.errors')

        # Configure Celery
        log.debug('Configuring Celery for handling tasks')
        configure_celery(celery_app, config.registry.settings)

        log.debug('Netwark webserver is configured!')
    return config.make_wsgi_app()
