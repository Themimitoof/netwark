import json

from pyramid.request import Request
from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPRequestTimeout,
    HTTPInternalServerError,
    HTTPMethodNotAllowed,
    HTTPServiceUnavailable,
)


@view_config(context=HTTPRequestTimeout)
@view_config(context=HTTPInternalServerError)
@view_config(context=HTTPNotFound)
@view_config(context=HTTPMethodNotAllowed)
@view_config(context=HTTPServiceUnavailable)
def http_exception(exc, request: Request):
    exceptions = {
        404: ('netwark:templates/404.pug', 'Route not found.'),
        403: (
            'netwark:templates/403.pug',
            'You are not allowed to access to this endpoint. '
            'Please check your apikey or your permissions.',
        ),
        405: (
            'netwark:templates/404.pug',
            'Method not available for this endpoint.',
        ),
        500: (
            'netwark:templates/500.pug',
            'An unexpected error happened on '
            'executing your request. Please retry more later.',
        ),
    }

    route = request.environ['PATH_INFO']

    if route.startswith('/api') or request.content_type == str(
        'application/json'
    ):
        # render json
        cause = exceptions.get(exc.code)[1]
        error = {'code': exc.code, 'cause': cause}

        response = Response(json.dumps(error))
        response.content_type = str('application/json')
        response.status_int = exc.code
        return response
    else:
        # render html
        response = render_to_response(exceptions.get(exc.code)[0], {})
        response.status_int = exc.code
        return response


@view_config(context=HTTPBadRequest)
def http_bad_request(exc, request: Request):
    route = request.environ['PATH_INFO']

    if route.startswith('/api') or request.content_type == str(
        'application/json'
    ):
        # render json
        error = {
            'code': exc.code,
            'cause': 'The request was not forged correctly. '
                     'Please see errors to fix your errors.',
            'errors': request.errors
        }

        response = Response(json.dumps(error))
        response.content_type = str('application/json')
        response.status_int = exc.code
        return response
    else:
        # render html
        response = render_to_response('netwark:templates/400.pug', {})
        response.status_int = exc.code
        return response
