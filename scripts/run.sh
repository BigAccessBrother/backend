#!/usr/bin/env bash
python manage.py migrate
python manage.py collectstatic --noinput
exec /opt/miniconda/envs/app/bin/uwsgi --ini /scripts/uwsgi.ini
