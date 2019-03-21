import os
import logging
import re
import subprocess
from ipaddress import ip_address

from pyramid.request import Request
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config
from pyramid.response import Response
from geoip2.database import Reader as geoip_reader

from sqlalchemy.exc import DBAPIError

from .. import models
from ..helpers import ip, asn

log = logging.getLogger(__name__)


@view_config(route_name="whois_main", renderer="../templates/whois/home.pug")
def whois_main_view(request: Request):
    return {'siteOptions': {'pageTitle': 'WHOIS'}, 'data': {}}


@view_config(
    route_name="whois_resource", renderer="../templates/whois/resource.pug"
)
def whois_resource_view(request: Request):
    resource = request.matchdict['resource']

    if asn.is_asn(resource):
        resource_type = 'asn'
        resource = resource.upper()
    # TODO: Add a validator or a regex for validating IDNs before
    # checking if is an ip address.
    elif ip.is_ip(resource):
        resource_type = 'ip'
    else:
        # TODO: Return to the previous page with "flash" error.
        return HTTPBadRequest()

    # Initialize data for the view
    data = {
        'type': resource_type,
        'resource': resource,
    }


    # Retrieve informations specific to the resource
    if resource_type == 'ip':
        data['whois_raw'] = ip.get_whois(resource)
        data['city'] = request.geoip_city(resource)
        data['asn'] = request.geoip_asn(resource)

        log.critical('city: %r', data['city'])

        # Retrieve PTR record
        ptr = ip.get_ptr(resource)
        data['reverse_dns'] = ptr.decode('utf-8')
    elif resource_type == 'asn':
        data['whois_raw'] = asn.get_whois(resource)

    return {
        'siteOptions': {'pageTitle': "Result of '{}'".format(resource)},
        'data': data,
    }
