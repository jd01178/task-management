#!/bin/sh

# wait for PSQL server to start
sleep 10

su -m myuser -c "/opt/venv/bin/python manage.py migrate"
su -m root -c "/opt/venv/bin/python -m gunicorn -b :8000 --workers 4 core.asgi:application -k uvicorn.workers.UvicornWorker"