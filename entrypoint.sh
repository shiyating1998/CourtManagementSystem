#!/bin/bash
set -e

# Start Redis server (optional: ensure Redis is ready before continuing)
echo "Starting Redis..."
redis-server &

# Start the Celery worker in the background
echo "Starting Celery worker..."
celery -A courtManagementSystem worker -l info -P eventlet --concurrency=1 &

# Run the Django app using exec to make it the main process
echo "Starting Django app with Gunicorn..."
exec "$@"
