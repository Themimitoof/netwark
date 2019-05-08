FROM python:3.7-alpine

COPY . /opt/netwark
WORKDIR /opt/netwark

RUN python -m venv /opt/netwark-venv && \
    source /opt/netwark-venv/bin/activate

RUN apk add --no-cache postgresql-client postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    /opt/netwark-venv/bin/pip install poetry && \
    /opt/netwark-venv/bin/poetry install --no-dev

RUN cp docker/entrypoint.sh /entrypoint.sh && \
    chmod +x /entrypoint.sh && \
    chown root:root /entrypoint.sh

ENTRYPOINT "/entrypoint.sh"

CMD pserve --reload development.ini
