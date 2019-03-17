from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models


@view_config(route_name="mac_oui", renderer="../templates/mac-oui.pug")
def mac_oui_view(request):
    return {
        'siteOptions': {
            'pageTitle': 'MAC OUI lookup'
        },
        'data': {}
    }

@view_config(route_name="api_mac_oui", renderer="json")
def api_mac_oui_view(request):
    return {}
