"""
Contains a suite of helpers and functions for domain names
"""
import logging
import re
import subprocess

import idna

log = logging.getLogger(__name__)


def is_valid_fqdn(fqdn: str) -> bool:
    """
    Check if the FQDN is valid.
    """
    # Regex friendly stealed from
    # https://github.com/johno/domain-regex/blob/8a6984c8fa1fe8481a4b99be0fa7f2a01ee17517/index.js
    pattern = re.compile(
        r'^\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b$'
    )

    return True if pattern.match(fqdn) else False


def to_idna(fqdn: str) -> str:
    """
    Converts the FQDN to IDNA
    """
    return fqdn.encode('idna').decode('utf-8')


def get_whois(resource: str) -> list:
    """
    Get WHOIS informations of the given domain

    :param resource: domain name
    :type resource: str

    :return: WHOIS result line by line
    :rtype: list
    """
    if is_valid_fqdn(resource):
        whois = subprocess.Popen(
            ['whois', resource], stdout=subprocess.PIPE
        ).stdout.read()

        return whois.decode('utf-8').split('\n')


def get_infos(whois: list) -> dict:
    """
    Parses domain informations from WHOIS return

    :param whois: get_whois return
    :type whois: list

    :return: A dict containing domain informations
    :rtype: dict
    """

    data = dict()

    for line in whois:
        if line == '':
            continue

        # Get registrar name
        if re.match(r'registrar:', line, re.IGNORECASE):
            data['registrar'] = re.sub(r'.*:\s+', '', line)

        # Get creation date
        if re.match(r'Creation Date:|created:', line, re.IGNORECASE):
            data['creation_date'] = re.sub(r'.*:\s+', '', line)

        # Get creation date
        if re.match(r'Updated Date:|last-update:', line, re.IGNORECASE):
            data['updated_date'] = re.sub(r'.*:\s+', '', line)

        # Get nameservers
        if re.match(r'Name Server:|nameserver:|nserver:', line, re.IGNORECASE):
            if 'nameservers' not in data:
                data['nameservers'] = list()

            data['nameservers'].append(
                re.sub(r'.*:\s+', '', line)
            )

    return data
