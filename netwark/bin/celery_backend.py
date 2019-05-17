import logging
import argparse
import sys

from celery import Celery
from pyramid.paster import bootstrap, setup_logging, get_appsettings

from netwark.backend import configure_celery
from netwark.helpers.ConfigRegistry import ConfigRegistry

log = logging.getLogger('netwark_worker')


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri', help='Configuration file, e.g., development.ini'
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    config = ConfigRegistry('netwark.app', get_appsettings(args.config_uri))

    log.info("Starting netwark backend")
    app = Celery(include=['netwark.backend.tasks'])
    configure_celery(app, config.configuration)

    # TODO: Make it modifiable with args
    worker_args = ['worker', '--loglevel=INFO', '--beat']

    app.worker_main(worker_args)


if __name__ == "__main__":
    main()
