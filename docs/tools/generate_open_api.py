"""
This script generates the Open API file used to autogenerate the documentation
for the REST API.
"""

import os
import argparse
import sys
import logging
import json

from pyramid.config import Configurator
from pyramid.paster import bootstrap, setup_logging, get_appsettings
from cornice.service import get_services
from cornice_swagger.swagger import CorniceSwagger

from netwark import __VERSION__

log = logging.getLogger('netwark')
doc_dir = os.path.dirname(os.path.realpath(__file__)) + '/..'


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri', help='Configuration file, e.g., development.ini'
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    app_settings = get_appsettings(args.config_uri)

    with Configurator(settings=app_settings) as config:
        log.info('Import cornice and APIv1 routes')
        config.include('cornice')
        config.include('netwark.api.v1')

        log.info('Generate the OpenAPI content')
        generator = CorniceSwagger(get_services())
        spec = generator('Netwark REST API', __VERSION__)

        # Fix the base path
        spec['basePath'] = '/api/v1'

        log.info('Store all the content into openapi.json file.')
        with open(doc_dir + '/openapi.json', 'w') as file:
            file.write(json.dumps(spec))

        log.info('Done.')
if __name__ == '__main__':
    main()
