#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py seed_from_frontend --if-empty

if [ "${DJANGO_COLLECTSTATIC:-0}" = "1" ]; then
  python manage.py collectstatic --noinput
fi

gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers "${GUNICORN_WORKERS:-3}" --timeout "${GUNICORN_TIMEOUT:-120}"
