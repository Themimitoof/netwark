from pyramid.view import view_config
from pyramid.response import Response

from ..models import Operation


@view_config(
    route_name="operations_list", renderer="../templates/operations/list.pug"
)
def operations_list_view(request):
    """
    Return a list of operations. By default, it return the lasts 50 operations
    and can be changed by using filters.

    TODO (next release): Create filters for this route.
    """

    session = request.dbsession

    query = (
        session.query(Operation)
        .order_by(Operation.updated_at.desc())
        .limit(50)
    )
    operations = []

    for operation in query:
        operation = operation.to_dict()

        if len(operation['queues']) > 3:
            operation['queues'] = operation['queues'][:3]
            operation['queues'].append("+")

        operations.append(operation)

    return {
        'siteOptions': {'pageTitle': 'List of operations'},
        'data': operations,
    }


@view_config(
    route_name="operations_info", renderer="../templates/operations/info.pug"
)
def operations_info_view(request):
    return {'siteOptions': {'pageTitle': 'Overview'}, 'data': {}}
