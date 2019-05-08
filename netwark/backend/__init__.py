import yaml
from celery import Celery
from kombu.common import Queue, Exchange, Broadcast


def configure_celery(app: Celery, app_settings):
    """
    Configure a Celery app with elements in configuration file.
    """
    with open(app_settings['backend.config'], 'r') as raw_config:
        config = yaml.load(raw_config, Loader=yaml.SafeLoader)

    app.config_from_object(config.get('celeryconfig'))

    # Configure queues
    queues = config.get('netwark_queues', None)

    default_exchange = Exchange(name='netwark', type='direct')
    broadcast_exchange = Broadcast('netwark.broadcast', 'netwark.broadcast')
    celery_queues = [
        Queue('netwark', default_exchange),
        broadcast_exchange,
    ]

    for queue in queues:
        if queue['queue'].startswith('netwark.'):
            queue_name = queue['queue']
        else:
            queue_name = 'netwark.' + queue['queue']

        if 'broadcast' in queue:
            celery_queues.append(Broadcast('netwark.broadcast', queue_name))
        else:
            celery_queues.append(Queue(queue_name, default_exchange))

    app.conf.task_queues = celery_queues
    return app
