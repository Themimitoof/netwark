import os
import sys
import logging
import argparse
from os import path
from subprocess import Popen
from hashlib import md5
import requests
from pyramid.paster import setup_logging, get_appsettings

log = logging.getLogger('netwark_update_oui_vendor_table')


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri', help='Configuration file, e.g., development.ini'
    )
    return parser.parse_args(argv[1:])


def download_new_db(settings):
    """
    Status download all new MaxMind DBs
    """
    asn_path = path.abspath(settings['geoip_database.asn'])
    city_path = path.abspath(settings['geoip_database.city'])

    # Download City database
    log.info('Downloading new version of City database...')
    city_download = requests.get(
        'https://geolite.maxmind.com/download/geoip/database/'
        'GeoLite2-City.tar.gz'
    )

    with open('/tmp/maxmind_city.tar.gz', 'wb') as temp_file:
        temp_file.write(city_download.content)

    # Download ASN database
    log.info('Downloading new version of ASN database...')
    asn_download = requests.get(
        'https://geolite.maxmind.com/download/geoip/database/'
        'GeoLite2-ASN.tar.gz'
    )

    with open('/tmp/maxmind_asn.tar.gz', 'wb') as temp_file:
        temp_file.write(asn_download.content)

    log.info('Uncompress tar archives')
    os.system('tar xzvf /tmp/maxmind_city.tar.gz -C /tmp')
    os.system('tar xzvf /tmp/maxmind_asn.tar.gz -C /tmp')

    log.info('Create destination folders if not exists')
    os.system('mkdir -p $(dirname {})'.format(settings['geoip_database.city']))
    os.system('mkdir -p $(dirname {})'.format(settings['geoip_database.asn']))

    log.info('Copy new databases to their destination folders')
    os.system('cp /tmp/GeoLite2-City*/*.mmdb ' + city_path)
    os.system('cp /tmp/GeoLite2-ASN*/*.mmdb ' + asn_path)

    # Delete temporary files
    log.info('Delete temporary files')
    os.system('rm -f /tmp/maxmind_*.tar.gz')


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    app_settings = get_appsettings(args.config_uri)

    download_new_db(app_settings)


if __name__ == "__main__":
    main()
