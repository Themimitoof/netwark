from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models


@view_config(route_name="whois_main", renderer="../templates/whois/home.pug")
def whois_main_view(request):
    return {
        'siteOptions': {
            'pageTitle': 'WHOIS'
        },
        'data': {}
    }


@view_config(
    route_name="whois_ressource", renderer="../templates/whois/ressource.pug"
)
def whois_ressource_view(request):
    return {
        'siteOptions': {
            'pageTitle': "Result of 'search'"
        },
        'data': {}
    }
