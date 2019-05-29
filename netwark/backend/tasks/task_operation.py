"""
Contains all tasks about operations
"""
import time
import logging
import json
import re

from subprocess import Popen, PIPE
from datetime import datetime, timedelta, timezone

import transaction

from sqlalchemy.sql.functions import now

from netwark import celery_app
from netwark.models import DBSession, Operation, OperationResult, gen_uuid
from netwark.backend import hostname

log = logging.getLogger(__name__)


@celery_app.task(name='netwark.operation', bind=True)
def run_operation(self, oper_id: str):
    session = DBSession()

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

    oper_id = operation.id
    oper_type = operation.type

    # Update the operation status if is still in pending
    if operation.status == 'pending':
        operation.status = 'progress'

        session.add(operation)
        session.flush()
        transaction.commit()
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
        id=gen_uuid(),
        operation_id=oper_id,
        worker=hostname,
        queue=queue,
        status='progress'
    )
    oper_result_id = oper_result.id

    # Commit the transaction for giving a feedback to the front
    session.add(oper_result)
    session.flush()
    transaction.commit()

    operation = (
        session.query(Operation).filter(Operation.id == oper_id).first()
    )

    # Execute the command
    if operation.type == 'ping':
        options = operation.options if operation.options else '-c10'

        command = ['ping']
        command.extend(options.split(' '))
        command.append(operation.target)
    elif operation.type == 'mtr':
        options = (
            operation.options + ' -j' if operation.options else '-bzj -c10'
        )

        command = ['mtr']
        command.extend(options.split(' '))
        command.append(operation.target)
    else:
        log.error(
            'Unable to execute %r because is not implemented on this version.',
            operation.type,
        )

        oper = session.query(OperationResult).filter(
            OperationResult.id == oper_result_id
        ).first()
        oper.status = 'error'
        oper.payload = {'cause': 'Tool not available on this worker.'}

        session.add(oper)
        session.flush()
        transaction.commit()
        return

    log.info('Running %r with options: %r', command[0], command[1])
    cmd = Popen(command, stdout=PIPE, stderr=PIPE)  # Run the command
    timeout_timer = time.time()
    update_timer = time.time()

    while cmd.poll() is None:
        # Put the task in timeout if is running more than 2 minutes or
        # update `updated_at` date every each 20 seconds
        if time.time() - timeout_timer >= 30:
            log.info(
                '%r is running since more than 2 minutes. Stop his '
                'execution.',
                oper_type,
            )

            oper = session.query(OperationResult).filter(
                OperationResult.id == oper_result_id
            ).first()
            oper.status = 'timeout'

            session.add(oper)
            session.flush()
            transaction.commit()
            cmd.kill()
            return
        elif time.time() - update_timer >= 20:
            update_timer = time.time()  # Reset the timer
            oper = session.query(OperationResult).filter(
                OperationResult.id == oper_result_id
            ).first()
            oper.updated_at = now()

            session.add(oper)
            session.flush()
            transaction.commit()

        time.sleep(2)

    if cmd.returncode == 0:
        if oper_type == 'ping':
            stdout = cmd.stdout.read().decode('utf-8').split('\n')
            db_payload = {
                'transmitted': 0,
                'received': 0,
                'duplicates': 0,
                'loss': 0,
                'min': 0,
                'max': 0,
                'average': 0,
                'raw': stdout,
            }

            stdout = stdout[-3:-1]  # Take only summary lines
            summary = stdout[0].split(', ')
            stats = re.findall(r'\d+.\d+', stdout[1])

            # Retrieve information from summary line
            for line in summary:
                if 'transmitted' in line:
                    db_payload['transmitted'] = int(
                        re.findall(r'\d+', line)[0]
                    )
                elif 'received' in line:
                    db_payload['received'] = int(re.findall(r'\d+', line)[0])
                elif 'duplicates' in line:
                    db_payload['duplicates'] = int(re.findall(r'\d+', line)[0])
                elif 'packet loss' in line:
                    db_payload['loss'] = float(
                        re.findall(r'\d+.\d+|\d+', line)[0]
                    )

            # Retrieve informations from stats line
            db_payload['min'] = float(stats[0])
            db_payload['average'] = float(stats[1])
            db_payload['max'] = float(stats[2])

            oper = session.query(OperationResult).filter(
                OperationResult.id == oper_result_id
            ).first()
            oper.status = 'done'
            oper.payload = db_payload

            session.add(oper)
            session.flush()
            transaction.commit()
        elif oper_type == 'mtr':
            stdout = cmd.stdout.read().decode('utf-8')

            try:
                db_payload = json.loads(stdout)
                result_status = 'done'
            except json.JSONDecodeError:
                db_payload = {
                    'stdout': stdout,
                    'stderr': [
                        'Unable to decode the report because is not '
                        'a JSON report.'
                    ],
                }

                result_status = 'error'

            oper = session.query(OperationResult).filter(
                OperationResult.id == oper_result_id
            ).first()
            oper.status = result_status
            oper.payload = db_payload

            session.add(oper)
            session.flush()
            transaction.commit()
    else:
        # Store the stdout and the stderr when the tool exit with a exit code
        # different of zero.
        db_payload = {
            'stdout': cmd.stdout.read().decode('utf-8').split('\n'),
            'stderr': cmd.stderr.read().decode('utf-8').split('\n'),
        }

        log.error('The tool was exited with a error message: %r', db_payload)

        oper = session.query(OperationResult).filter(
            OperationResult.id == oper_result_id
        ).first()
        oper.status = 'error'
        oper.payload = db_payload

        session.add(oper)
        session.flush()
        transaction.commit()


@celery_app.task(name='netwark.check_operations_statuses')
def check_operations_statuses():
    """
    Check the status of all operations and update it if is too old or all
    workers have not sent any data for more than 45 seconds.
    """
    session = DBSession()

    log.info('Start checking operations statuses...')

    # Cleanup all pending operations not started hat have more than 2 minutes
    query = session.query(Operation).filter(Operation.status == 'pending')

    for operation in query:
        # Not needed to check if entries are on operation_result because, the
        # status is automatically changed on the first execution by a worker.
        updated_at_delta = operation.updated_at + timedelta(minutes=2)

        if datetime.utcnow() > updated_at_delta:
            log.info(
                '%r has not been updated for more than 2 minutes.',
                operation.id,
            )
            operation.status = 'timeout'
            session.add(operation)

    session.flush()
    transaction.commit()

    # Manage all "in progress" tasks
    operations = session.query(Operation).filter(
        Operation.status == 'progress'
    )

    for operation in operations:
        oper_results = session.query(OperationResult).filter(
            OperationResult.operation_id == operation.id
        )

        still_progress = False
        last_updated = datetime.fromtimestamp(0)

        for oper in oper_results:
            # If the operation status stalled, updated it.
            # Normally, the backend updated his "updated_at" every 20 seconds
            updated_at_delta = oper.updated_at + timedelta(minutes=1)
            if (
                oper.status == 'progress'
                and datetime.utcnow() > updated_at_delta
            ):
                log.info(
                    'Operation result %r timed out (no update for 1 minute)',
                    oper.id,
                )
                oper.status = 'timeout'
                session.add(oper)

            if oper.status == 'progress':
                still_progress = True

            if oper.updated_at > last_updated:
                last_updated = oper.updated_at

        last_updated_delta = last_updated + timedelta(minutes=1)
        if (
            not still_progress
            and datetime.utcnow() > last_updated_delta
        ):
            log.info(
                'Operation %r have not received any update for 1 minute',
                operation.id,
            )
            operation.status = 'done'
            session.add(operation)

    session.flush()
    transaction.commit()

    # Cleaning operations results that the operation are not in progress
    oper_results = session.query(OperationResult).filter(
        OperationResult.status == 'progress'
    )

    for oper in oper_results:
        updated_at_delta = oper.updated_at + timedelta(minutes=2)
        if datetime.utcnow() > updated_at_delta:
            log.info(
                'Oper result %r have not received any update for 2 minutes',
                oper.id,
            )
            oper.status = 'timeout'

            session.add(oper)

    session.flush()
    transaction.commit()
