#!/bin/sh

flask db init
flask db migrate -m "migrate at the docker"
flask db upgrade

gunicorn -b "auth-server:8000" "app:create_app()"
