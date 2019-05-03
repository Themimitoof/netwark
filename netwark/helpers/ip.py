"""
Contains a suite of helpers and functions for IP addresses
"""

import subprocess
import logging
import ipaddress

log = logging.getLogger(__name__)


def is_ip(resource: str) -> bool:
    """
    Check if the resource is a valid IPv4/IPv6 address.

    :param resource: IPv4/v6 address
    :type resource: str

    :rtype: bool
    """
    try:
        ipaddress.ip_address(resource)

        return True
    except:
        return False


def ip_type(resource: str) -> dict:
    """
    Returns the type of IP address
    """
    try:
        ip = ipaddress.ip_address(resource)
        version = 6 if type(ip) == ipaddress.IPv6Address else 4
    except:
        raise Exception('Given IP address not valid.')

    if ip.is_global:
        return {'version': version, 'public': True, 'type': 'global'}
    elif ip.is_link_local:
        return {'version': version, 'public': False, 'type': 'link_local'}
    elif ip.is_loopback:
        return {'version': version, 'public': False, 'type': 'loopback'}
    elif ip.is_multicast:
        return {'version': version, 'public': False, 'type': 'multicast'}
    elif ip.is_private:
        return {'version': version, 'public': False, 'type': 'private'}
    elif ip.is_reserved:
        return {'version': version, 'public': False, 'type': 'reserved'}
    elif version == 6 and ip.is_site_local:
        return {'version': 6, 'public': False, 'type': 'site_local'}
    elif version == 6 and ip.sixtofour:
        return {'version': 6, 'public': True, 'type': '6to4'}
    elif version == 6 and ip.teredo:
        return {'version': 6, 'public': False, 'type': 'teredo'}
    else:
        return {'version': version, 'public': False, 'type': 'special'}


def get_ptr(resource: str) -> str:
    """
    Get reverse DNS (PTR) entry of the given IP address

    :param resource: IPv4/v6 address
    :type resource: str

    :return: PTR entry
    :rtype: str
    """
    if is_ip(resource):
        ptr = subprocess.Popen(
            ['dig', '+short', '-x', resource],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if ptr.wait() == 0:
            return ptr.stdout.read().decode('utf-8').replace('\n', '')
        else:
            raise Exception(
                'dig error code: {} - message: {}'.format(
                    ptr.poll(), ptr.stderr.read().decode('utf-8')
                )
            )
    else:
        raise Exception('Given IP address not valid.')


def get_whois(resource: str) -> list:
    """
    Get WHOIS informations of the given IP address

    :param resource: IPv4/v6 address
    :type resource: str

    :return: WHOIS result line by line
    :rtype: list
    """
    if is_ip(resource):
        if ip_type(resource)['public']:
            whois = subprocess.Popen(
                ['whois', resource], stdout=subprocess.PIPE
            ).stdout.read()

            return whois.decode('utf-8').split('\n')


def get_subnet_informations(resource):
    """
    Return all informations about the requested network.
    """
    ip_str, cidr = resource.split('/')
    ip_version = ip_type(ip_str)['version']
    cidr = int(cidr)

    if ip_version == 6:
        ip = ipaddress.IPv6Network(resource, strict=False)

        output = {
                'network': str(ip.network_address),
                'cidr': cidr,
                'usable_ips': ip.num_addresses - 1,
                'first_ip': str(ip.network_address + 1),
                'last_ip': '',
            }

        if cidr == 127:
            output['usable_ips'] = 2
        elif cidr == 128:
            output['usable_ips'] = 1
        else:
            output['first_ip'] = str(ip.network_address + 1)
            output['last_ip'] = str(ip.broadcast_address)

        if cidr >= 127:
            output.pop('first_ip')
            output.pop('last_ip')
            output.pop('broadcast')
    else:  # IPv4
        ip = ipaddress.IPv4Network(resource, strict=False)

        output = {
                'network': str(ip.network_address),
                'netmask': str(ip.netmask),
                'cidr': cidr,
                'usable_ips': ip.num_addresses - 2,
                'first_ip': '',
                'last_ip': '',
                'broadcast': str(ip.broadcast_address)
            }

        if cidr == 31:
            output['usable_ips'] = 2
        elif cidr == 32:
            output['usable_ips'] = 1
        else:
            output['first_ip'] = str(ip.network_address + 1)
            output['last_ip'] = str(ip.broadcast_address - 1)

        if cidr > 30:
            output.pop('first_ip')
            output.pop('last_ip')
            output.pop('broadcast')

    return output
