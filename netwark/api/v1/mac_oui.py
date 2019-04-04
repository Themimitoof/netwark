import re

import colander
from cornice.resource import resource, view
from cornice.validators import colander_validator

from .. import APIBase
from ..context import APIContext

mac_regex = r"^([a-zA-Z0-9]{6,12}|([a-zA-Z0-9]{2}[:-]){2,5}[a-zA-Z0-9]{2})$"


# --- Schemas
class GetAPIParams(colander.MappingSchema):
    @colander.instantiate(name='querystring')
    class QueryString(colander.MappingSchema):
        assignment = colander.SchemaNode(
            colander.String(),
            missing=colander.drop,
            validator=colander.Regex(mac_regex)
        )
        orgname = colander.SchemaNode(colander.String(), missing=colander.drop)


# --- Validators
def validate_assign():
    pass


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
        permission='',
        schema=GetAPIParams,
        validators=(colander_validator,),
    )
    def get(self):
        return {}
