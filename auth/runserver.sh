#!/bin/sh

flask db init
flask db migrate

gunicorn -b "auth-server:8000" "app:create_app()"
