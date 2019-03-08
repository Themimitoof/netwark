from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models


@view_config(route_name="overview", renderer="../templates/overview.pug")
def overview_view(request):
    return {
        'pageTitle': 'Overview',
    }
