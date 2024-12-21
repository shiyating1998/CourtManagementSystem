#!/bin/bash
set -e

# Environment variables with defaults
DB_HOST="${DB_HOST:-mysql_db}"
DB_PORT="${DB_PORT:-3306}"
DB_USER="${DB_USER:-user}"
DB_PASSWORD="${DB_PASSWORD:-password}"
DB_NAME="${DB_NAME:-court_management_system}"

echo "Waiting for MySQL database..."

# Wait for MySQL to be ready
until mysqladmin ping -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" --silent; do
    echo "MySQL is unavailable - sleeping"
    sleep 5
done

echo "MySQL is up and running!"



if [ "$RUN_MIGRATIONS" = "true" ]; then
    # Apply database migrations
    echo "Applying database migrations..."
    python manage.py makemigrations
    python manage.py migrate
fi

# Collect static files if needed
if [ "$DJANGO_COLLECT_STATIC" = "true" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

# Start the main application
echo "Starting application..."
exec "$@"