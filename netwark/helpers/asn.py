"""
Contains a suite of helpers and functions for Asynchronous System Numbers (ASN)
"""

import subprocess
import logging
import re

log = logging.getLogger(__name__)


def is_asn(resource: str) -> bool:
    """
    Check if the resource is a valid AS number.

    :param resource: AS number
    :type resource: str

    :rtype: bool
    """

    if re.match(r'^AS\d{1,10}$', resource, re.IGNORECASE):
        return True
    else:
        return False


def get_whois(resource: str) -> list:
    """
    Get WHOIS informations of the given ASN

    :param resource: AS number
    :type resource: str

    :return: WHOIS result line by line
    :rtype: list
    """
    if is_asn(resource):
        whois = subprocess.Popen(
            ['whois', resource], stdout=subprocess.PIPE
        ).stdout.read()

        return whois.decode('utf-8').split('\n')


def get_infos(whois: list) -> dict:
    """
    Parses organization informations from WHOIS return

    :param whois: get_whois return
    :type whois: list

    :return: A dict containing organization informations
    :rtype: dict
    """
    objects = {
        'RIPE': {  # Europe
            'as': 'aut-num',
            'name': 'as-name',
            'org': 'org-name',
        },
        'APNIC': {  # Asia
            'as': 'aut-num',
            'name': 'as-name',
            'org': 'org-name',
        },
        'ARIN': {  # North America
            'as': 'ASNumber',
            'name': 'ASName',
            'org': 'OrgName',
        },
        'LACNIC': {  # South America
            'as': 'aut-num',
            'name': 'ownerid',
            'org': 'owner',
        },
        'AFRINIC': {  # Africa
            'as': 'aut-num',
            'name': 'as-name',
            'org': 'org-name',
        },
    }

    # Detect RIR

    for line in whois:
        for el in objects.keys():
            rir = el if el in line else None
            continue

        if rir:
            continue

    data = dict()

    import pdb; pdb.set_trace()

    # Get other informations
    for line in whois:
        if objects[rir]['as'] in line:
            data['asn'] = line
        elif objects[rir]['name'] in line:
            data['name'] = line
        elif objects[rir]['org'] in line:
            data['org'] = line

    data['rir'] = rir

    return data
