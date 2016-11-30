from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heartbeat.settings')

app = Celery(
    'heartbeat',
    broker='redis://localhost:6379/0',
    backend='redis://localhost',
    task_serializer='json',
    result_serializer='json'
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if __name__ == '__main__':
    app.start()