#!/bin/sh

# wait for Redis server to start
sleep 10

# Replace * with name of Django Project
su -m myuser -c "/opt/venv/bin/celery -A core.background beat -l info --pidfile=/tmp/core.pid"