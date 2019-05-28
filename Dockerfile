FROM node:lts-alpine AS build-env

COPY . /opt/netwark
WORKDIR /opt/netwark

RUN npm i && \
    ./node_modules/.bin/gulp

FROM python:3.7-alpine

COPY . /opt/netwark
COPY --from=build-env /opt/netwark/dist /opt/netwark/dist
WORKDIR /opt/netwark

RUN apk add --no-cache \
        postgresql-client \
        postgresql-libs \
        bash \
        mtr \
        uwsgi \
        uwsgi-python3 && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install poetry pasteScript


RUN cp docker/entrypoint.sh /entrypoint.sh && \
    chmod +x /entrypoint.sh && \
    chown root:root /entrypoint.sh

RUN addgroup -g 1100 netwark && \
    adduser -h /opt/netwark -G netwark -u 1101 -D netwark

USER netwark

RUN poetry install --no-dev

EXPOSE 6543

CMD poetry run pserve config/production.ini

# Prepare the ground for using uwsgi instead of pserve.
# For the moment, it not work because uwsgi doesn't find paste module.
#CMD uwsgi --plugin=python3 -H /opt/netwark/.cache/pypoetry/virtualenvs/netwark-py3.7/ -M --workers 2 --enable-threads --http-socket 127.0.0.1:6543 --listen 64 --paste=config:/opt/netwark/config/development.ini --paste-logger
