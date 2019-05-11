import sys
import traceback
import logging

import colander
from pyramid.exceptions import HTTPBadRequest, HTTPNotFound
from pyramid.httpexceptions import HTTPInternalServerError
from cornice.resource import resource, view
from cornice.validators import (
    colander_querystring_validator,
    colander_path_validator,
    colander_body_validator,
)

from .. import APIBase
from ..context import APIContext
from netwark import celery_app
from netwark.models import DBSession, Operation, OperationResult
from netwark.models.operation import OPERATION_FLAGS, operation_status
from netwark.backend import is_broker_available
from netwark.backend.tasks import run_operation

log = logging.getLogger(__name__)


# --- Validators
def load_operation(request, **kwargs):
    """
    Load the operation informations from the database
    """
    params = request.validated
    session = DBSession(request.registry.settings)

    operation = (
        session.query(Operation)
        .filter(Operation.id == params['operation_id'])
        .first()
    )

    if not operation:
        request.errors.add(
            'path', 'resource_id', 'resource_id not found in database'
        )

    request.validated['operation'] = operation


# --- Schemas
class GetCollectionAPIParams(colander.MappingSchema):
    page = colander.SchemaNode(colander.Integer(), missing=0)
    per_page = colander.SchemaNode(
        colander.Integer(), validator=colander.Range(1, 1000), missing=50
    )
    status = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(operation_status.enums),  # pylint:disable-all
        missing=colander.drop,
    )
    type = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(OPERATION_FLAGS),
        missing=colander.drop,
    )


class GetAPIParams(colander.MappingSchema):
    operation_id = colander.SchemaNode(
        colander.String(),
        # TODO: Add UUID regex. validator=colander.UUID_REGEX
    )


class PostAPIParams(colander.MappingSchema):
    type = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(OPERATION_FLAGS),  # pylint:disable-all
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
            session.query(Operation).order_by(Operation.created_at.desc())
            # TODO: Create the pagination system
            # and send some informations in response headers
            # .limit(params['per_page'])
            # .offset(params['page'] * params['per_page'])
        )

        if 'status' in params:
            query = query.filter(Operation.status == params['status'])

        if 'type' in params:
            query = query.filter(Operation.type == params['type'])

        return [operation.to_dict() for operation in query.all()]

    @view(
        renderer='json',
        schema=GetAPIParams,
        validators=(colander_path_validator, load_operation),
    )
    def get(self):
        """
        Returns informations about the operation and the result from all
        workers.
        """
        params = self.request.validated
        operation = params['operation']
        session = DBSession(self.request.registry.settings)

        # Retrieve operation results
        operation_results = (
            session.query(OperationResult)
            .filter(OperationResult.operation_id == Operation.id)
            .all()
        )

        output = operation.to_dict()
        output['results'] = []

        for oper_result in operation_results:
            output['results'].append(
                {
                    'status': oper_result.status,
                    'worker': oper_result.worker,
                    'queue': oper_result.queue,
                    'payload': oper_result.payload,
                    'updated_at': oper_result.updated_at.strftime(
                        '%Y-%m-%d %H:%M:%S.%f'
                    ),
                    'created_at': oper_result.created_at.strftime(
                        '%Y-%m-%d %H:%M:%S.%f'
                    ),
                }
            )

        return output

    @view(
        renderer='json',
        schema=PostAPIParams,
        validators=(colander_body_validator),
    )
    def collection_post(self):
        """
        Create new operation with the informations received in parameters

        TODO: For queues, use the dict for matching with existing queues
        """
        params = self.request.validated
        session = DBSession(self.request.registry.settings)

        operation = Operation(
            type=params['type'], target=params['target'], status='pending'
        )

        # Manage queues
        if 'queues' not in params:
            operation.queues = 'netwark.broadcast'
        else:
            for queue in params['queues']:
                if not queue.startswith('netwark.'):
                    queue = 'netwark.' + queue

                if operation.queues:
                    operation.queues = operation.queues + ',' + queue
                else:
                    operation.queues = queue

        if 'options' in params:
            operation.options = params['options']

        # Create the operation in database
        if is_broker_available(celery_app):
            log.info('Create new operation %r', operation)
            try:
                session.add(operation)
                session.commit()

                # Push the task into the queue
                queues = operation.queues.split(',')

                for queue in queues:
                    log.info(
                        'Pushing task %r for the queue %r.',
                        operation.id,
                        queue,
                    )

                    run_operation.apply_async(
                        kwargs={'oper_id': operation.id},
                        queue=queue,
                        retry=False,
                    )
            except Exception as err:
                log.critical(
                    'Unable to create operation on database or an eror '
                    'was occured with the broker.'
                )
                traceback.print_exc(file=sys.stdout)
                session.rollback()
                raise HTTPInternalServerError
        else:
            raise HTTPInternalServerError

        return {'message': 'Operation created', 'operation_id': operation.id}
