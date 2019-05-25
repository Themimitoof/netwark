Install on a server
===================
*We consider you already have deployed RabbitMQ and PostgreSQL and have
installed everything on your servers.*

General instructions
--------------------
The very beginning step is to clone or download an archive of the latest
version of Netwark. If you want to use git, simply clone the repo by using:

.. code-block:: bash

    git clone --branch <tag_name> https://github.com/themimitoof/netwark netwark
    cd netwark

*The list of tags are available on GitHub.*


If you prefer using ``tar`` or ``zip`` archives, you can download one by using
the `release page`_ on GitHub.

.. _`release page`: https://github.com/Themimitoof/netwark/releases

You can now create a *Python virtualenv* and activate it by using:

.. code-block:: bash

    python3 -m venv venv && source venv/bin/activate

.. warning::
    If the module ``venv`` is not available, you can install it by installing
    the packet ``python3-venv`` on Ubuntu/Debian, shipped by default on Fedora/CentOS.

We need now to download ``Poetry`` for downloading all our dependencies:

.. code-block:: bash

    pip install poetry && \  # Install poetry on the virtualenv
    poetry install --no-dev  # Retrieve all dependencies only needed for a production environment.

.. note::
    If you want to test ``master`` branch, a in-progress feature or simply
    contribute to the codebase, you should remove ``--no-dev`` to the list of
    arguments sent to ``poetry``.

A good part is now finished. You can now follow next sections to finish the
deployment of each part of Netwark.


Deploy the Webserver
--------------------
Before continuing the deployment, we need to create a ``.mapbox-token`` file at
the root folder of Netwark  that contain the **access token** of
your Mapbox account.

Now, you can download all *front-end* dependencies by using ``npm``
and *bundle* all resources with:

.. code-block:: bash

    npm i && \
    ./node_modules/.bin/gulp all


Deploy the worker
-----------------
fdsfsfs


Install on Docker
=================
fdsfds
