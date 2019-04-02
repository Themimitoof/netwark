import logging
import argparse
import sys
import re

import requests
from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from netwark.models import OuiVendor

log = logging.getLogger(__name__)
oui_url = 'http://standards-oui.ieee.org/oui/oui.csv'


# Downloadable
def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri', help='Configuration file, e.g., development.ini'
    )
    return parser.parse_args(argv[1:])


def retrieve_csv_file():
    """
    Get OUI Vendor file from http://standards-oui.ieee.org/oui/oui.csv and
    serializes it for the next operation.
    """
    log.info('Retrieve updated OUI vendor file from %s', oui_url)

    req = requests.get(oui_url)

    # If everything is OK
    if req.status_code == 200:
        text = req.text
        exploded = text.split('\r\n')
        output = []

        for line in exploded:
            pattern = re.compile(r"((?:[^,\"']|\"[^\"]*\"|'[^']*')+)")
            line = pattern.split(pattern)[1::2]
            line.pop(0)  # Remove the registry entry
            log.critical(line)
            output.append(line)

        # Remove the header of the file and the last empty line
        output.pop(0).pop(-1)
        return output
    else:
        raise requests.HTTPError()


def update_database():
    """
    Updates the OUI vendor table with the new data.
    """
    pass


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)

    retrieve_csv_file()
    update_database()


if __name__ == "__main__":
    main()
