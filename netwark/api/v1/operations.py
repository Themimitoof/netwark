import logging

import colander
from pyramid.exceptions import HTTPBadRequest, HTTPNotFound
from cornice.resource import resource, view
from cornice.validators import (
    colander_querystring_validator,
    colander_path_validator,
)

from .. import APIBase
from ..context import APIContext
from netwark.models import DBSession, Operation, OperationResult
from netwark.models.operation import OPERATION_FLAGS, operation_status
from netwark.backend.tasks import run_operation

log = logging.getLogger(__name__)


# --- Schemas
class GetCollectionAPIParams(colander.MappingSchema):
    page = colander.SchemaNode(colander.Integer(), missing=0)
    per_page = colander.SchemaNode(
        colander.Integer(), validator=colander.Range(1, 1000), missing=50
    )
    status = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(OPERATION_FLAGS),
        missing=colander.drop,
    )
    type = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(operation_status.enums),  # pylint:disable-all
        missing=colander.drop,
    )


class GetAPIParams(colander.MappingSchema):
    operation_id = colander.SchemaNode(
        colander.String(), validator=colander.UUID_REGEX
    )


class PostAPIParams(colander.MappingSchema):
    type = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(operation_status.enums),  # pylint:disable-all
    )
    target = colander.SchemaNode(colander.String())
    options = colander.SchemaNode(colander.String(), missing=colander.drop)

    @colander.instantiate(name='queues', missing=colander.drop)
    class QueuesSequence(colander.SequenceSchema):
        _ = colander.SchemaNode(colander.String())


# --- Routes
@resource(
    collection_path='/operations',
    path='/operations/{operation_id}',
    name='api_v1_operations',
    factory=APIContext,
)
class ApiOperations(APIBase):
    @view(
        renderer='json',
        schema=GetCollectionAPIParams,
        validators=(colander_querystring_validator),
    )
    def collection_get(self):
        params = self.request.validated
        session = DBSession(self.request.registry.settings)

        query = (
            session.query(Operation)
            .order_by(Operation.created_at.desc())
            .limit(params['per_page'])
            .offset(params['page'] * params['per_page'])
        )

        if 'status' in params:
            query = query.filter(Operation.status == params['status'])

        if 'type' in params:
            query = query.filter(Operation.type == params['type'])

        return [operation.to_dict() for operation in query.all()]
