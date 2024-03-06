#!/bin/sh

flask db init
flask db migrate -m "migrate at the docker"
flask db upgrade

gunicorn -b "contents-server:8000" "app:create_app()"
