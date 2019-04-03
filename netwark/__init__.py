from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pyramid.events import NewRequest

from .events import flash_messages


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('pypugjs.ext.pyramid')
        config.include('.geoip')
        config.include('.routes')

        # Configure session factory
        session_factory = SignedCookieSessionFactory(
            config.registry.settings['session.token']
        )
        config.set_session_factory(session_factory)

        # Add operation glags to request methods
        def operation_flags(request):
            return ['ping', 'mtr']

        config.add_request_method(
            operation_flags, 'operation_flags', reify=True
        )

        # Execute flash_messages method when a new request happen
        config.add_subscriber(flash_messages, NewRequest)

        config.scan()

    return config.make_wsgi_app()
