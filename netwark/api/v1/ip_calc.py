import logging
import re

import colander
from pyramid.exceptions import HTTPBadRequest, HTTPNotFound
from cornice.resource import resource, view
from cornice.validators import (
    colander_path_validator,
)

from .. import APIBase
from ..context import APIContext
from netwark.helpers.ip import get_subnet_informations

log = logging.getLogger(__name__)


# --- Schemas
class GetAPIParams(colander.MappingSchema):
    resource = colander.SchemaNode(colander.String())
    cidr = colander.SchemaNode(colander.Integer())


# --- Routes
@resource(
    path='/ip-calc/{resource}/{cidr}',
    name='api_v1_ip_calc',
    factory=APIContext,
)
class ApiIPCalc(APIBase):
    @view(
        renderer='json',
        schema=GetAPIParams,
        validators=(colander_path_validator,)
    )
    def get(self):
        try:
            return get_subnet_informations('{}/{}'.format(
                self.request.validated['resource'],
                self.request.validated['cidr'],
            ))
        except Exception as err:
            self.request.errors.add('path', err.__class__.__name__, str(err))
