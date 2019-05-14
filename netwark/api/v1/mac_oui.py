import logging
import re

import colander
from pyramid.exceptions import HTTPBadRequest, HTTPNotFound
from cornice.resource import resource, view
from cornice.validators import (
    colander_querystring_validator,
    colander_path_validator,
)

from .. import APIBase
from ..context import APIContext
from netwark.models import OuiVendor

log = logging.getLogger(__name__)

mac_regex = re.compile(
    r"^([a-f0-9]{6,12}|([a-f0-9]{2}[:-]){2,5}[a-f0-9]{2})$", re.IGNORECASE
)

mac_like_regex = re.compile(
    r"^[a-f0-9]{1,12}|([a-f0-9]{2}[:-]){1,5}[a-f0-9]{1,2}$", re.IGNORECASE
)


# --- Helpers
def truncate_macaddr(request, **kwargs):
    """
    Truncate the received mac address to get only the assignment part.
    """

    def truncate(resource, strict=False):
        regex = mac_regex if strict else mac_like_regex

        if re.match(regex, resource):
            resource = re.sub(r'[:-]', '', resource)[:6]
            return resource, True
        else:
            return resource, False

    if 'resource' in request.validated:
        request.validated['is_macaddr'] = False
        resource = request.validated['resource']

        resource, is_macaddr = truncate(resource, True)
        request.validated['resource'] = resource
        request.validated['is_macaddr'] = is_macaddr
    elif 'assignment' in request.validated:
        resource = request.validated['assignment']

        resource, _is_macaddr = truncate(resource)
        request.validated['assignment'] = resource


# --- Schemas
class GetCollectionAPIParams(colander.MappingSchema):
    assignment = colander.SchemaNode(
        colander.String(),
        missing=colander.drop,
        validator=colander.Regex(mac_like_regex),
    )
    orgname = colander.SchemaNode(colander.String(), missing=colander.drop)


class GetAPIParams(colander.MappingSchema):
    resource = colander.SchemaNode(colander.String(), missing=colander.drop)


# --- Routes
@resource(
    collection_path='/mac-oui',
    path='/mac-oui/{resource}',
    name='api_v1_mac_oui',
    factory=APIContext,
)
class ApiMacOUI(APIBase):
    @view(
        renderer='json',
        schema=GetCollectionAPIParams,
        validators=(colander_querystring_validator, truncate_macaddr),
    )
    def collection_get(self):
        session = self.request.dbsession

        if (
            'assignment' not in self.request.validated
            and 'orgname' not in self.request.validated
        ):
            db = session.query(OuiVendor).all()
        else:
            assignment = self.request.validated.get('assignment', None)
            orgname = self.request.validated.get('orgname', None)

            db = session.query(OuiVendor)

            if assignment:
                db = db.filter(OuiVendor.assignment.like(assignment + '%'))

            if orgname:
                db = db.filter(OuiVendor.orgname.like(orgname + '%'))

            db = db.all()

        return [entry.to_dict() for entry in db]

    @view(
        renderer='json',
        schema=GetAPIParams,
        validators=(colander_path_validator, truncate_macaddr),
    )
    def get(self):
        session = self.request.dbsession
        resource = self.request.validated['resource']

        if self.request.validated['is_macaddr']:
            db = (
                session.query(OuiVendor)
                .filter(OuiVendor.assignment == resource)
                .first()
            )
        else:
            db = (
                session.query(OuiVendor)
                .filter(OuiVendor.orgname == resource)
                .first()
            )

        if db:
            return db.to_dict()
        else:
            return {}
