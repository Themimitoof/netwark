import logging

from pyramid.config import Configurator
from geoip2.database import Reader, MODE_MEMORY

log = logging.getLogger(__name__)


def configure_geoip_readers(config: Configurator):
    """
    Set GeoIP readers in memory and expose them with request_methods.
    """
    city_db = config.registry.settings['geoip_database.city']
    asn_db = config.registry.settings['geoip_database.asn']

    city_reader = Reader(city_db, None, MODE_MEMORY)
    asn_reader = Reader(asn_db, None, MODE_MEMORY)

    def get_city(_request, resource):
        return city_reader.city(resource)

    def get_asn(_request, resource):
        return asn_reader.asn(resource)

    config.add_request_method(get_city, 'geoip_city', reify=False)
    config.add_request_method(get_asn, 'geoip_asn', reify=False)


def includeme(config):
    log.debug('Configuring GeoIP readers...')
    configure_geoip_readers(config)
