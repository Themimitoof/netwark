import socket
import logging

import yaml

from celery import Celery
from kombu import Connection
from kombu.common import Queue, Exchange, Broadcast

log = logging.getLogger(__name__)
hostname = socket.gethostname()
backend_queues = []


def configure_celery(app: Celery, app_settings):
    """
    Configure a Celery app with elements in configuration file.
    """
    from netwark.backend.tasks.task_operation import check_operations_statuses

    with open(app_settings['backend.config'], 'r') as raw_config:
        config = yaml.load(raw_config, Loader=yaml.SafeLoader)

    app.config_from_object(config.get('celeryconfig'))

    # Configure queues
    queues = config.get('netwark_queues', None)

    default_exchange = Exchange(name='netwark', type='direct')
    broadcast_exchange = Broadcast('netwark.broadcast', 'netwark.broadcast')
    celery_queues = [Queue('netwark', default_exchange), broadcast_exchange]

    for queue in queues:
        if not queue['queue'].startswith('netwark.'):
            queue['queue'] = 'netwark.' + queue['queue']

        queue_name = queue['queue']
        backend_queues.append(queue)  # Insert the queue into a reusable list

        if 'broadcast' in queue and queue['broadcast'] is True:
            celery_queues.append(
                Broadcast(queue_name, '{}@{}'.format(queue_name, hostname))
            )
        else:
            queue['broadcast'] = False
            celery_queues.append(Queue(queue_name, default_exchange))

    app.conf.task_queues = celery_queues

    # Configure periodic tasks
    log.info(
        'Configuring check_operations_statuses task to be executed '
        'every 60 seconds.'
    )
    app.add_periodic_task(60.0, check_operations_statuses.s())

    return app


def is_broker_available(app):
    """
    Checks if the broker is available by initializing a connection with them.
    """
    broker_url = app.conf['broker_url']

    try:
        conn = Connection(broker_url)
        conn.ensure_connection(max_retries=1)
        return True
    except Exception as err:
        log.critical('An error is occured with the broker. Message: %r', err)
    else:
        return False
