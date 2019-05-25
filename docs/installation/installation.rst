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

You can go now into the ``config`` folder and create a copy of all files or
``netwark_backend.yaml.example`` and ``<environment>.ini.example``, and remove
the ``.example`` in the extension.

For now, you can edit in ``netwark_backend.yaml`` the line ``broker_url:`` and
replace the connection string by your *RabbitMQ* credentials.

In the ``<environment>.ini`` file, replace the connection string in
``sqlalchemy.url`` with our *PostgreSQL* credentials.

Your installation is almost ready to use! If you want, you can pause the
deployment to continue to configuring the webserver by following the
`configuration page`_.


.. _`alembic migrations`:

Now, we need to run our database migrations scripts. For this, we only need to
run the command ``alembic -c config/<environment>.ini upgrade head``.

After that, we need to retrieve latest version of *MaxMind DB* and updating the
*MAC OUI* database. For this, run theses two commands:

.. code-block:: bash

    python netwark/bin/update_oui_vendor_table.py config/<environment>.ini
    python netwark/bin/update_maxmind_db.py config/<environment>.ini

Everything is now configured! Congratulations! But we need to configure a last
thing system side. Before continuing, you can test if the webserver works by
typing the command:

.. code-block:: bash

    pserve config/<environment>.ini

You can now open your browser and go to http://localhost:6543.

Use supervisord
^^^^^^^^^^^^^^^
You can use supervisord as daemon manager. For this, create a new
``netwark-webserver.conf`` in ``/etc/supervisor/conf.d`` folder or add at the
end of ``/etc/supervisord.conf`` file, the below content:

.. code-block:: ini

    [program:netwark-webserver]
    command=<uwsgi command>
    directory=/opt/netwark ; Replace with the good path

    autostart=true
    autorestart=true
    startretries=20
    stdout_logfile=/var/log/netwark/netwark-webserver.log
    redirect_stderr=true

You can now reload the configuration or restart ``supervisord`` by typing:

.. code-block:: ini

    pkill -SIGHUP -x supervisord
    # or
    systemctl restart supervisord
    # or
    service supervisor restart
    # or
    /etc/init.d/supervisor restart

Now, you should have access to the webserver through your web browser by
accessing to http://localhost:6543. If is not, check the logs specified in the
``supervisord`` configuration file.

Use systemd
^^^^^^^^^^^
The main Linux distributions embed ``systemd`` by default. To use it, create a
new service by creating a new file on
``/etc/systemd/system/netwark-webserver.service`` and add the below content:

.. code-block:: ini

    [Unit]
    Description=Netwark webserver
    Requires=Network.target
    After=network.target

    [Service]
    Type=simple
    ExecStart=<uwsgi command>
    StandardOutput=file:/var/log/netwark/netwark-webserver.log
    StandardError=file:/var/log/netwark/netwark-webserver-errors.log

You can now check if the service start and work well by using the command
``systemctl start netwark-webserver`` and by accessing to http://localhost:6543
with your browser.

If the webserver works, you can enable the service to start automatically on
boot:

.. code-block:: bash

    systemctl enable netwark-webserver


Voilà! You have done the deployment of the werbserver! We recommand to follow the
`configuration page`_ to adjust your installation.

Deploy the worker
-----------------
The deployment of the worker is more easier than the webserver because it
doesn't need much steps.

First above, you need to go into the ``config`` folder and create a copy of all
files or ``netwark_backend.yaml.example`` and ``<environment>.ini.example``,
and remove the ``.example`` in the extension.

For now, you can edit in ``netwark_backend.yaml`` the line ``broker_url:`` and
replace the connection string by your *RabbitMQ* credentials.

In the ``<environment>.ini`` file, replace the connection string in
``sqlalchemy.url`` with our *PostgreSQL* credentials.

If you dont have runned the database migrations wet, you need to run it by
using the command:

.. code-block:: bash

    alembic -c config/<environment>.ini upgrade head

The worker is now ready to start! To test before creating the service
configuration, you can start it by using the command:

.. code-block:: bash

    python netwark/bin/celery_backend.py config/<environment>.ini


Use supervisord
^^^^^^^^^^^^^^^
You can use supervisord as daemon manager. For this, create a new
``netwark-worker.conf`` in ``/etc/supervisor/conf.d`` folder or add at the
end of ``/etc/supervisord.conf`` file, the below content:

.. code-block:: ini

    [program:netwark-worker]
    command=<path to bin folder of your virtualenv>/python /opt/netwark/netwark/bin/celery_backend.py /opt/netwark/config/<environment>.ini
    directory=/opt/netwark ; Replace with the good path

    autostart=true
    autorestart=true
    startretries=20
    stdout_logfile=/var/log/netwark/netwark-webserver.log
    redirect_stderr=true

.. note::
    Please take care to replace the path in the configuration file by the good
    path used in your server.

You can now reload the configuration or restart ``supervisord`` by typing:

.. code-block:: ini

    pkill -SIGHUP -x supervisord
    # or
    systemctl restart supervisord
    # or
    service supervisor restart
    # or
    /etc/init.d/supervisor restart

You can now ``tail`` the logs file and run a new operation through the web
interface or via the *REST API*.


Use systemd
^^^^^^^^^^^
The main Linux distributions embed ``systemd`` by default. To use it, create a
new service by creating a new file on
``/etc/systemd/system/netwark-worker.service`` and add the below content:

.. code-block:: ini

    [Unit]
    Description=Netwark worker daemon
    Requires=Network.target
    After=network.target

    [Service]
    Type=simple
    ExecStart=<path to bin folder of your virtualenv>/python /opt/netwark/netwark/bin/celery_backend.py /opt/netwark/config/<environment>.ini
    StandardOutput=file:/var/log/netwark/netwark-worker.log
    StandardError=file:/var/log/netwark/netwark-worker-errors.log

.. note::
    Please take care to replace the path in the configuration file by the good
    path used in your server.

You can now start the worker by using ``systemctl start netwark-worker`` and
follow the logs by using ``tail`` or with ``journalctl`` and run a new
operation through the web interface or via the *REST API*.

.. code-block:: bash

    tail -f /var/log/netwark/netwark-worker.log /var/log/netwark/netwark-worker-errors.log

    # or

    journalctl -f netwark-worker

If the worker execute the task without error, you can enable the service to
start automatically on boot by using:

.. code-block:: bash

    systemctl enable netwark-worker


Voilà! You have done the deployment of the worker! We recommand to follow the
`configuration page`_ to adjust your installation.

Install on Docker
=================
fdsfds


.. _`configuration page`: configuration