# Netwark: A Netadmin tool for lazy netadmins
Netwark is a web-based toolkit for lazy systems and network administrators that want to run parellized tools on multiple servers.

Netwark can help you to run `ping` or `mtr` on a single machine, all machines of the network or a group of machines. It embed some tools like **IPv4/IPv6 calculator**, **MAC OUI Lookup** and can **WHOIS** _domains, ASN and ip addresses_.

In the future, it's planned to add more tools and the capability to create _smoke pings_ graphs and alerts.

# Deployment informations
Netwark is completly written in Python using [Pyramid Framework](https://trypyramid.com/), [Cornice](http://cornice.readthedocs.io/), [Celery](https://docs.celeryproject.org/en/latest) and uses PostgreSQL has database.

**Requirements:**
 * **Linux/Unix host**: the server can works on _Windows_ but the worker need some commands that only work on a true _Linux/Unix_ environment (WSL don't allow to play with raw sockets).
 * **PostgreSQL** 9.5+
 * **RabbitMQ**
 * **Node.JS** LTS (only for needed for _npm and gulp_)

You can also deploy Netwark on **Docker** and scale as you want.

For more informations, check the [documentation](https://netwark.readthedocs.io/en/latest/).

# Documentation
The installation and configuration instructions are available on our documentation page on: [https://netwark.readthedocs.io/en/latest/](https://netwark.readthedocs.io/en/latest/).


# Contributions
Netwark is free and open source software licensed under **MIT** license.

You can open issues to report a bug, suggest a new feature/enhancement or open a pull request to contribute to the codebase.

Please ensure you have [black](https://github.com/python/black), [pylint](https://github.com/PyCQA/pylint), [pycodestyle](https://github.com/PyCQA/pycodestyle) and [eslint](https://github.com/eslint/eslint) installed on your machine and ensure that no errors are returned by theses tools. Please create or adapt tests units for all your modifications.