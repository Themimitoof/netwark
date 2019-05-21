.. Netwark documentation master file, created by
   sphinx-quickstart on Wed Mar 27 15:17:05 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Netwark's documentation!
===================================

.. toctree::

   architecture
   installation/index
   rest_api/index



Netwark is a web-based toolkit for lazy systems and network administrators that want to run parellized tools on multiple servers.
Netwark can help you to run ping or mtr on a single machine, all machines of the network or a group of machines. It embed some tools like IPv4/IPv6 calculator, MAC OUI Lookup and can WHOIS domains, ASN and ip addresses.

In the future, it's planned to add more tools and the capability to create smoke pings graphs and alerts.


Deployment informations
-----------------------
Netwark is completly written in Python using `Pyramid Framework`_, Cornice_, Celery_ and uses PostgreSQL has database.

 .. _`Pyramid Framework`: https://trypyramid.com/
 .. _Cornice: http://cornice.readthedocs.io/
 .. _Celery: https://docs.celeryproject.org/en/latest

Requirements:
 * **Linux/Unix host** the server can works on Windows but the worker need some commands that only work on a true Linux/Unix environment (WSL don't allow to play with raw sockets).
 * **PostgreSQL** 9.5+
 * **RabbitMQ**
 * **Node.JS** LTS (only for needed for npm and gulp)

You can also deploy Netwark on Docker and scale as you want.

For more informations, check the documentation.


Contributions
-------------
Netwark is free and open source software licensed under **MIT** license.

You can open issues to report a bug, suggest a new feature/enhancement or open a pull request to contribute to the codebase.

Please ensure you have black_, pylint_, pycodestyle_ and ESLint_ installed on your machine and ensure that no errors are returned by theses tools. Please create or adapt tests units for all your modifications.

.. _black: https://github.com/python/black
.. _pylint: https://github.com/PyCQA/pylint
.. _pycodestyle: https://github.com/PyCQA/pycodestyle
.. _ESLint: https://github.com/eslint/eslint

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
