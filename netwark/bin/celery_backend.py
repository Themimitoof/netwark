import logging
import argparse
import sys

from celery import Celery
from pyramid.paster import bootstrap, setup_logging, get_appsettings

from netwark.backend import configure_celery

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
    app_settings = get_appsettings(args.config_uri)

    print("Starting netwark backend")
    app = Celery(include=['netwark.backend.tasks'])
    configure_celery(app, app_settings)

    # TODO: Make it modifiable with args
    worker_args = [
        'worker',
        '--loglevel=INFO',
    ]

    app.worker_main(worker_args)


if __name__ == "__main__":
    main()
