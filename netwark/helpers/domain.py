"""
Contains a suite of helpers and functions for domain names
"""
import logging
import re

import idna

log = logging.getLogger(__name__)


def is_valid_fqdn(fqdn: str) -> bool:
    """
    Check if the FQDN is valid.
    """
    # Regex friendly stealed from
    # https://github.com/kvesteri/validators/blob/fa3cb286f617fd4523b3ff28c1da8617d6028bfb/validators/domain.py
    pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )

    return True if pattern.match(fqdn) else False


def to_idna(fqdn: str) -> str:
    """
    Converts the FQDN to IDNA
    """
    return fqdn.encode('idna').decode('utf-8')
