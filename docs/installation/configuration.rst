Configuration
=============
This page contains all information you need to add additional settings to
your installation.

<environment>.ini files
-----------------------
This configuration file contains all information the worker and the webserver
need to work.

In general, two keys are important:

- `sqlalchemy.url`: contain the connection string to the PostgreSQL server
- `backend.config`: contain the path to the `netwark_backend.yaml` file

.. note::
    SQLAlchemy give you the possibility to use several databases types. We do
    not recommend to use other database engine. If you still want to use for
    example MySQL, please make a pile of tests and send us a *Pull request* to
    integrate the database engine to the list of compatible database engines.

For the webserver, some additional keys are important to edit/keep update:

- `session.token`: this is the token for signing your user sessions. Please
  change his value before exposing the webserver to your network.
- `geoip_database.city`: contain the path to the MaxMind City database. The
  presence of the database is needed to start the webserver because is a key
  feature for retrieving additional informations when you WHOIS IP addresses
  and ASN.
- `geoip_database.ASN`: same as `geoip_database.city` but for the MaxMind ASN
  database.

If you are not satisfied with the output of the logs of the webserver or for
the worker, you can edit the *logging* configuration by following the guide
available on the *pyramid* documentation: https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/logging.html


netwark_backend.yaml file
-------------------------
This configuration file is specific to asynchronous tasks. Both our components
need them to send operations to queues (webserver) and listen queues for
receiving and executing operations (worker).

Every keys in the object `celeryconfig` are configuration keys of Celery. The
complete list are available on https://docs.celeryproject.org/en/latest/userguide/configuration.html.

This part is not recommended to modify except three keys:

- `broker_url`: contain the connection string to the RabbitMQ broker.
- `timezone`: update it to use your timezone/server timezone
- `broker_heartbeat`: specify the interval time between the worker need to send
  a *heartbeat* signal (we recommend to keep 60 seconds).

The `netwark_queues` are more important to configure. It concern all the queues
of the worker can listen tasks. By default, every workers listen `netwark`
queue and `netwark.broadcast` queue. `netwark` queue is a simple *direct* queue
that RabbitMQ dispatch the task like *round-robin*. The `netwark.broadcast`
queue is a *broadcastable* queue. All tasks sent to this queue are
automatically played by **all workers** connected to the queue.

We have choosed to purpose a way to seperate where you want to execute your
tasks by purposing the creation of custom queues. The best scenario is
creating multiple queues for separating each offices/datacenters/circuits.

To do this, we have a template available on the example file.

.. code-block:: yaml

    netwark_queues:
        - queue: lc_eqx_pa2
          name: 'Equinix PA2'
          location: '114 Rue Ambroise Croizat, 93200 Saint-Denis, France'
          broadcast: true

- *queue*: is the name of the queue in Celery. To avoid errors, we only
  recommend to follow AMQP recommendations and uses ``[a-zA-Z0-9-_.:]``
  characters.
- *name*: this is the name of the queue/location. This label will be soon
  visible on the frontend.
- *location*: this key give location informations to the frontend. Same as the
  name label, it will be soon visible on the frontend.
- *broadcast (not mandatory - default: False)*: specify if the queue need to
  be configured as a *broadcast* queue.

.. warning::
    All queues you specify on your workers need to be specified in the
    `netwark_backend.yaml` file of the *webserver*. If you don't fill with all
    queues, you will do able not send operations to theses queues.
