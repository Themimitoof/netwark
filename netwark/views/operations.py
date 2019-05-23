import uuid

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from ..models import DBSession, Operation, OperationResult


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
        'siteOptions': {
            'pageTitle': 'List of operations',
            'flash': request.flash,
        },
        'data': operations,
    }


@view_config(
    route_name="operations_info", renderer="../templates/operations/info.pug"
)
def operations_info_view(request):
    # Retrieve operation informations
    session = DBSession()
    oper_id = request.matchdict['uuid']

    try:
        _ = uuid.UUID(oper_id)
    except ValueError:
        request.session['flash'] = [
            {'type': 'invalid_uuid', 'severity': 'error'}
        ]

        return HTTPFound(location=request.route_url('operations_list'))

    # Retrieve operation informations
    operation = (
        session.query(Operation).filter(Operation.id == oper_id).first()
    )

    if not operation:
        request.session['flash'] = [
            {'type': 'oper_not_found', 'severity': 'warning'}
        ]

        return HTTPFound(location=request.route_url('operations_list'))

    results = {}

    # Return operations results
    oper_results = session.query(OperationResult).filter(
        OperationResult.operation_id == operation.id
    )

    for result in oper_results:
        if result.queue not in results:
            results[result.queue] = list()

        results[result.queue].append(result)

    return {
        'siteOptions': {
            'pageTitle': 'Overview of the operation ({} - {})'.format(
                operation.type, operation.target
            )
        },
        'data': {'operation': operation.to_dict(), 'results': results},
    }
