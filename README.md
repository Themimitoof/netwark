# Netwark: A Netadmin tool for lazy netadmins
Netwark was made for all people who want to have a network toolbox in their browser/phone with some additionnal cool stuff like _smokeping_, _multi zone ping_ and _mtr_.

# Getting Started
- Create a Python virtual environment.
```bash
python3 -m venv env
```

- Upgrade packaging tools.
```bash
env/bin/pip install --upgrade pip setuptools
```

- Install the project in editable mode with its testing requirements.
```bash
env/bin/pip install -e ".[testing]"
```

- Initialize and upgrade the database using Alembic.
    - Generate your first revision.
    ```bash
    env/bin/alembic -c development.ini revision --autogenerate -m "init"
    ```

    - Upgrade to that revision.
    ```bash
    env/bin/alembic -c development.ini upgrade head
    ```

- Load default data into the database using a script.
```bash
env/bin/initialize_netwark_db development.ini
```

- Run your project's tests.
```bash
env/bin/pytest
```

- Run your project.
```bash
env/bin/pserve development.ini
```