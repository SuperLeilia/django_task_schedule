import os
from celery import Celery
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_task_schedule.settings')

app = Celery('django_task_schedule')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.now = timezone.now