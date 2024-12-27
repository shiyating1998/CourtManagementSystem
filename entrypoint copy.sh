#!/bin/bash
set -e

# if [ "$RUN_MIGRATIONS" = "true" ]; then
#     # Apply database migrations
#     echo "Applying database migrations..."
#     python manage.py makemigrations
#     python manage.py migrate

#     # Create superuser if environment variables are set
#     if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
#         echo "Creating superuser..."
#         python manage.py createsuperuser --noinput \
#             --username $DJANGO_SUPERUSER_USERNAME \
#             --email $DJANGO_SUPERUSER_EMAIL
#     fi
# fi

# Start the main application
echo "Starting application..."

# Start Redis server in the background
redis-server &

# Run Django app in the background
python manage.py runserver 0.0.0.0:8000 &
# Run Celery worker
celery -A courtManagementSystem worker -l info -P eventlet --concurrency=1