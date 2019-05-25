Prerequisites
=============

Netwark is designed for Linux/Unix systems. Running the webserver or a worker
on Windows are not officially supported and we haven’t tested it. Running
the worker on the *Windows Subsystem Linux* not work because some tools need
*raw sockets manipulation*, not available on the current version of WSL.

If you still want to deploy Netwark on a Windows environment, you can use
Docker. It can resolve the problem of OS incompatibility, but it can be painful
for deploying the networking part.

Because Netwark is mainly focused for an internal use, it doesn't have (yet)
any authentication et authorization mechanisms. We do not recommend to expose
the webserver on Internet to avoid attacks.

If your infrastructure allows you to create a dedicated network connected to
all your regions, we recommend to do it.

Infrastructure prerequisites
----------------------------
Netwark need some external services for storing the data and for communicating
with the entire network of workers.

Netwark need these services installed on the same host of the webserver or on
separate servers (recommended):

- RabbitMQ_ >= 3.5
- PostgreSQL_ >= 9
- Internet connectivity. This point seems stupid, but if you want to retrieve
  information from public resources, you need Internet. More information are
  added on the next sections.

For each nodes, you need to install:

- Python >= 3.5, we use python types, not working with previous versions
- Poetry_, Poetry seems largely better than Pipenv/Pipfile
- PostgreSQL libs (needed for communicating with the database)
- Ping utility (we use it for... pinging machines)
- WHOIS utility (we use it in synchronous and asynchronous tasks for
  retrieving information of a public resource of Internet)
- dig utility (we use it for retrieving informations from DNS zones and for
  reverse DNSs)


Webserver prerequisites
-----------------------
Because the webserver doesn't run magic tools (only normal stuff), the
webserver can be installed on a Windows machine but it's recommended.

You need to install on the host in addition of the packages specified in the
last section:

- NodeJS (for retrieving and handling frontend assets)
- A reverse proxy server (e.g. Apache, Nginx). Exposing the uwsgi/waitress
  are not recommended.
- Mapbox_ account for showing the maps
- Internet connectivity. We need Internet for all *synchronous tasks* and for
  updating the database (MAC OUI database) and retrieving new versions of
  *Maxmind databases*.


Worker prerequisites
--------------------
The worker is a magical part of the project that listen constantly RabbitMQ
queues that his assigned, ready to run the instructions sent through into
the queues.

The worker need some magical tools and the listen can increase with the time
and the next releases.

For this release, each machine hosting a worker need:

- *mtr*, basically a much better *traceroute/ping* utility.
- *ping*, for receiving ``pong`` from other machines
- Internet connectivity. Unlike the webserver, the worker doesn't need big
  requirements in term of bandwidth and traffic needs. In case you are in a
  cloud environment, you can dedicate few gigabytes (1-2GB) of traffic per
  months. Of course, it will depend with the usage you will have with Netwark.

.. _RabbitMQ: https://www.rabbitmq.com/
.. _PostgreSQL: https://www.postgresql.org/docs/
.. _Poetry: https://poetry.eustace.io/
.. _Mapbox: https://mapbox.com
