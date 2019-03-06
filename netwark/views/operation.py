from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models


@view_config(
    route_name="operation_new", renderer="../templates/operation_new.pug"
)
def operation_new_view(request):
    return {}


@view_config(
    route_name="operation_info", renderer="../templates/operation_info.pug"
)
def operation_info_view(request):
    return {}
