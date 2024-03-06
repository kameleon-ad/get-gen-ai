#!/bin/sh

flask db init
flask db migrate -m "migrate at the docker"
flask db upgrade

gunicorn -b "$HOST:$PORT" "app:create_app()"
