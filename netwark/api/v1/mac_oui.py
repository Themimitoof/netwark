import logging
import re

import colander
from pyramid.exceptions import HTTPBadRequest
from cornice.resource import resource, view
from cornice.validators import colander_querystring_validator

from .. import APIBase
from ..context import APIContext

log = logging.getLogger(__name__)

mac_regex = re.compile(
    r"^([a-z0-9]{6,12}|([a-z0-9]{2}[:-]){2,5}[a-z0-9]{2})$", re.IGNORECASE
)


# --- Schemas
class GetAPIParams(colander.MappingSchema):
        assignment = colander.SchemaNode(
            colander.String(),
            missing=colander.drop,
            validator=colander.Regex(mac_regex),
        )
        orgname = colander.SchemaNode(colander.String(), missing=colander.drop)


# --- Validators
def validate_assign(request, **kwargs):
    if (
        'assignment' not in request.validated and
        'orgname' not in request.validated
    ):
        request.errors.add(
            'querystring',
            '*',
            "Please specify 'assignment' or 'orgname' value.",
        )

    log.critical(request.validated)


# --- Routes
@resource(
    path='/mac-oui',
    name='api_v1_mac_oui',
    factory=APIContext
    # error_handler=
)
class ApiMacOUI(APIBase):
    @view(
        renderer='json',
        schema=GetAPIParams,
        validators=(colander_querystring_validator, validate_assign),
    )
    def get(self):
        return {}
