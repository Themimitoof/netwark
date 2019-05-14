import logging
import re

import colander
from cornice.resource import resource, view

from .. import APIBase
from ..context import APIContext
from netwark.backend import backend_queues

log = logging.getLogger(__name__)


# --- Routes
@resource(
    collection_path='/management/backend/queues',
    path='/management/backend/queues/{queue}',
    name='api_v1_management_backend_queues',
    factory=APIContext,
)
class ApiManagementBackendQueuesOUI(APIBase):
    @view(
        renderer='json'
    )
    def collection_get(self):
        return backend_queues
