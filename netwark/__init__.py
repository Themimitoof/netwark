from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('pypugjs.ext.pyramid')
        config.include('.geoip')
        config.include('.routes')

        def operation_flags(request):
            return ['ping', 'mtr', 'whois']

        config.add_request_method(
            operation_flags, 'operation_flags', reify=True
        )
        config.scan()
    return config.make_wsgi_app()
