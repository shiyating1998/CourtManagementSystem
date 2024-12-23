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

#!/bin/bash

if [ "$DYNO" = "worker" ]
then
    celery -A courtManagementSystem worker -l INFO -P eventlet --concurrency=1
else
    CMD gunicorn courtManagementSystem.wsgi:application --bind 0.0.0.0:$PORT
fi

