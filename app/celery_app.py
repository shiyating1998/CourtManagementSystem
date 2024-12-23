# myproject/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import eventlet
import ssl 
eventlet.monkey_patch()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courtManagementSystem.settings')

# Get the Redis URL from environment variable
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Celery configuration
CELERY_BROKER_URL = REDIS_URL + '?ssl_cert_reqs=CERT_NONE'
CELERY_RESULT_BACKEND = REDIS_URL + '?ssl_cert_reqs=CERT_NONE'      

# Set up SSL options for rediss:// scheme
if REDIS_URL.startswith("rediss://"):
    CELERY_BROKER_TRANSPORT_OPTIONS = {
        "ssl": {
            "ssl_cert_reqs": ssl.CERT_NONE  # or ssl.CERT_OPTIONAL or ssl.CERT_REQUIRED
        }
    }

app = Celery('courtManagementSystem')
#app = Celery('courtManagementSystem', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='UTC', #TODO
    enable_utc=True,
)