"""
Contains all tasks about operations
"""
import time
import logging

from subprocess import Popen, PIPE
from datetime import datetime, timedelta

from sqlalchemy.sql.functions import now

from netwark import celery_app
from netwark.helpers.ConfigRegistry import ConfigRegistry
from netwark.models import DBSession, Operation, OperationResult
from netwark.backend import hostname

log = logging.getLogger(__name__)


@celery_app.task(name='netwark.operation', bind=True)
def run_operation(self, oper_id: str):
    config = ConfigRegistry('netwark.app')
    session = DBSession(config.configuration)

    log.info('Running task for the operation %r', oper_id)

    operation = (
        session.query(Operation).filter(Operation.id == oper_id).first()
    )

    # Check if the operation in available in the database
    if not operation:
        retries = 0

        while retries >= 4:
            retries += 1
            log.info(
                'Retry to retrieve the operation informations. Attempt %d/3',
                retries,
            )

            operation = (
                session.query(Operation)
                .filter(Operation.id == oper_id)
                .first()
            )

            if not operation:
                log.operation('Operation still not found...')
                time.sleep(10)

        if not operation:
            return

    # Update the operation status if is still in pending
    if operation.status == 'pending':
        operation.status = 'progress'
        session.add(operation)
        session.commit()
    elif operation.status in ['timeout', 'error', 'done']:
        return

    # Determine the queue name with the exchange (broadcast) or the
    # routing_key (normal queues)
    if self.request.delivery_info['exchange']:
        queue = self.request.delivery_info['exchange']
    elif self.request.delivery_info['routing_key']:
        queue = self.request.delivery_info['routing_key']
    else:
        queue = 'unknown'

    # Create the worker entry in operation_result table
    oper_result = OperationResult(
        operation_id=operation.id,
        worker=hostname,
        queue=queue,
        status='progress',
    )
    session.add(oper_result)
    session.commit()

    # Execute the command
    if operation.type == 'ping':
        options = operation.options if operation.options else '-c10'
        cmd = Popen(['ping', options, operation.target], stdout=PIPE, stderr=PIPE)
    elif operation.type == 'mtr':
        options = operation.options if operation.options else '-c10 -bzrj'
        log.info('mtr command')
    else:
        log.error(
            'Unable to execute %r because is not implemented on this version.',
            operation.type,
        )
        oper_result.status = 'error'
        oper_result.payload = {'cause': 'Non implemented tool on this worker.'}
        return

    timer = time.time()  # Start a timer to log when the command was runned

    while cmd.poll() != 0:
        log.info(cmd.stdout.read().decode('utf-8'))
        log.info(cmd.stderr.read().decode('utf-8'))

        if cmd.poll() == 0:
            log.info(cmd.stdout.read().decode('utf-8'))
        else:
            # Put the task in timeout if is running more than 2 minutes or
            # update `updated_at` date every each 20 seconds
            if timer - time.time() >= 120:
                log.info(
                    '%r is running since more than 2 minutes. Stop his '
                    'execution.',
                    operation.type,
                )
                oper_result.status = 'timeout'
                oper_result.updated_at = now()
                session.commit()
                cmd.terminate()
            elif timer - time.time() >= 20:
                oper_result.updated_at = now()
                session.add(oper_result)
                session.commit()

            time.sleep(2)


@celery_app.task(name='netwark.check_operations_statuses')
def check_operations_statuses():
    """
    Check the status of all operations and update it if is too old or all
    workers have not sent any data for more than 45 seconds.
    """
    config = ConfigRegistry('netwark.app')
    session = DBSession(config.configuration)

    log.info('Start checking operations statuses...')

    # Cleanup all pending operations not started hat have more than 2 minutes
    query = session.query(Operation).filter(Operation.status == 'pending')

    for operation in query:
        # Not needed to check if entries are on operation_result because, the
        # status is automatically changed on the first execution by a worker.
        if (operation.updated_at + timedelta(minutes=2)) < datetime.now():
            log.info(
                '%r has not been updated for more than 2 minutes.',
                operation.id,
            )
            operation.status = 'timeout'
            operation.updated_at = now()
            session.add(operation)

    session.commit()

    # Manage all "in progress" tasks
    # query = session.query(Operation).filter(Operation.status == 'progress')

    # for operation in query:
