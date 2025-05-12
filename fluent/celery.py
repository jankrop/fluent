
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fluent.settings')

app = Celery('fluent', backend='redis://localhost', broker='redis://localhost')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()