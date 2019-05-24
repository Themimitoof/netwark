FROM node:lts-alpine AS build-env

COPY . /opt/netwark
WORKDIR /opt/netwark

RUN npm i && \
    ./node_modules/.bin/gulp

FROM python:3.7-alpine

COPY . /opt/netwark
COPY --from=build-env /opt/netwark/dist /opt/netwark/dist
WORKDIR /opt/netwark

RUN apk add --no-cache postgresql-client postgresql-libs bash mtr && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install poetry


RUN cp docker/entrypoint.sh /entrypoint.sh && \
    chmod +x /entrypoint.sh && \
    chown root:root /entrypoint.sh

RUN addgroup -g 1100 netwark && \
    adduser -h /opt/netwark -G netwark -u 1101 -D netwark

USER netwark

RUN poetry install --no-dev

CMD poetry run pserve production.ini
