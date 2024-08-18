#!/bin/bash

poetry run python manage.py migrate

poetry run python manage.py collectstatic --noinput

poetry run python create_superuser.py

exec "$@"
