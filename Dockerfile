FROM python:3.7-alpine

COPY . /opt/netwark
WORKDIR /opt/netwark

RUN python -m venv /opt/netwark-venv && \
    source /opt/netwark-venv/bin/activate

RUN apk add --no-cache postgresql-client postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install poetry && \
    poetry install --no-dev

CMD pserve --reload development.ini
