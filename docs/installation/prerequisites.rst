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
  added in the next sections.

On each nodes, you need to install:

- Python >= 3.5 (We uses python types, not working with previous versions)
- PostgreSQL libs (needed for communicating with the database)
- Ping utility (we uses it for... pinging machines)
- WHOIS utility (we uses it in synchronous and asynchronous tasks for
  retrieving informations of a public resource of Internet)
- dig utility (we uses it for retrieving informations from DNS zones and for
  reverses IPs)


Webserver prerequisites
-------------------------------
Because the webserver don't run magic tools (only normal stuff), the webserver
can be installed on a Windows machine but it's recommended.

You need to install on the host in addition of the packages specified on the
last section:

- NodeJS (for retrieving and handling frontend assets)
- A reverse proxy server (e.g. Apache, Nginx). Exposing the uwsgi/waitress
  are not recommended.
- Internet connectivity. We need Internet for all *synchronous tasks* and for
  updating the database (MAC OUI database) and retrieving new versions of
  *Maxmind databases*.


Worker prerequisites
----------------------------
The worker


.. _RabbitMQ: https://www.rabbitmq.com/
.. _PostgreSQL: https://www.postgresql.org/docs/
