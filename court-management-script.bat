@echo off
REM Start Django service
start cmd /k ".venv\Scripts\activate && python manage.py runserver 8000"

REM Start Redis
start cmd /k "C:\Software\Redis-x64-3.0.504\redis-server.exe"

REM Start Celery worker
start cmd /k ".venv\Scripts\activate && celery -A courtManagementSystem worker -l info -P eventlet"

REM Start Stripe webhook
start cmd /k "stripe listen --forward-to localhost:8000/webhooks/stripe/"
