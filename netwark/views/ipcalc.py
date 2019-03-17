from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models


@view_config(route_name="ipcalc", renderer="../templates/ipcalc.pug")
def ipalc_view(request):
    return {
        'siteOptions': {
            'pageTitle': 'IP Calculator'
        },
        'data': {}
    }
