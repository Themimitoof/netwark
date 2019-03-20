import logging
import re
from ipaddress import ip_address

from pyramid.request import Request
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models

log = logging.getLogger(__name__)


@view_config(route_name="whois_main", renderer="../templates/whois/home.pug")
def whois_main_view(request: Request):
    return {
        'siteOptions': {
            'pageTitle': 'WHOIS'
        },
        'data': {}
    }


@view_config(
    route_name="whois_resource", renderer="../templates/whois/resource.pug"
)
def whois_resource_view(request: Request):
    resource = request.matchdict['resource']

    try:
        if re.match(r'^AS\d{1,10}$', resource, re.IGNORECASE):
            resource_type = 'asn'
            resource = resource.upper()
        # TODO: Add a validator or a regex for validating IDNs before
        # checking if is an ip address.
        elif ip_address(resource):
            resource_type = 'ip'
    except:
        # TODO: Return to the previous page with "flash" error.
        return HTTPBadRequest()

    return {
        'siteOptions': {
            'pageTitle': "Result of '{}'".format(resource)
        },
        'data': {
            'type': resource_type,
            'resource': resource,
            'whois_raw': ''
        }
    }
