from pyramid.view import view_config
from pyramid.response import Response


@view_config(
    route_name="operations_list", renderer="../templates/operations/list.pug"
)
def operations_list_view(request):
    return {}


@view_config(
    route_name="operations_info", renderer="../templates/operations/info.pug"
)
def operations_info_view(request):
    return {}
