import logging
import argparse
import sys
import re

import requests
from pyramid.paster import bootstrap, setup_logging, get_appsettings
from sqlalchemy.exc import OperationalError

from netwark.models import OuiVendor, DBSession

log = logging.getLogger('netwark_update_oui_vendor_table')
oui_url = 'http://standards-oui.ieee.org/oui/oui.csv'


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri', help='Configuration file, e.g., development.ini'
    )
    return parser.parse_args(argv[1:])


def retrieve_csv_file() -> list:
    """
    Get OUI Vendor file from http://standards-oui.ieee.org/oui/oui.csv and
    serializes it for the next operation.
    """
    log.info('Retrieve updated OUI vendor file from %s', oui_url)

    req = requests.get(oui_url)

    # If everything is OK
    if req.status_code == 200:
        text = req.text
        exploded = text.split(' \r\n')
        output = []

        exploded.pop(0)  # Remove the header
        exploded.pop(-1)  # Remove the last empty line

        for line in exploded:
            pattern = re.compile(r"((?:[^,\"']|\"[^\"]*\"|'[^']*')+)")
            line = pattern.split(line)

            # Remove the registry entry, comma separator and empty string
            line = list(filter(lambda i: i not in [',', ''], line))
            line.pop(0)  # Remove the registry entry

            # Remove quotes on orgname and orgaddr
            for i, item in enumerate(line):
                line[i] = re.sub(r"(^\")|(\"$)", '', item)

            if len(line) == 2:
                line.append(None)

            output.append(line)

        return output
    else:
        raise requests.HTTPError()


def update_database(data: list, settings):
    """
    Updates the OUI vendor table with the new data.
    """
    session = DBSession(settings)

    for line in data:
        log.info("Merge %s - %s (%s)", line[0], line[1], line[2])
        oui = OuiVendor(assignment=line[0], orgname=line[1], orgaddr=line[2])
        session.merge(oui)

    session.commit()


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    app_settings = get_appsettings(args.config_uri)

    data = retrieve_csv_file()
    update_database(data, app_settings)
    log.info('Update done.')


if __name__ == "__main__":
    main()
