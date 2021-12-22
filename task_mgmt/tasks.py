from celery import shared_task
from django_celery_beat.models import PeriodicTask
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from task_mgmt.cron_util import create_periodic_task
from .models import Message, Task

import random


@shared_task
def remove_expired_tasks():
    tasks = PeriodicTask.objects.all()
    for task in tasks:
        if task.expires is not None and task.expires < timezone.now():
            task_obj = Task.objects.get(id=int(task.name))
            task_obj.status = 2
            task_obj.save()
            task.enabled = False
            task.save()
            task.delete()


@shared_task
def schedule_periodic_task(task_id, task_type, execute_time, week, month_of_year, day_of_month):
    create_periodic_task(task_id, 'task_mgmt.tasks.generate_num_periodic', task_type, execute_time, week, month_of_year, day_of_month)


@shared_task
def generate_num_periodic(task_id):
    num = random.uniform(0, 1000)
    Message.objects.create(
        task_id=task_id,
        time=timezone.now(),
        message='Task {0}:\t{1}'.format(task_id, str(round(num, 2)))
    )
    task = Task.objects.get(id=task_id)
    task.status = 1
    task.save()


@shared_task
def generate_num_once(task_id):
    num = random.uniform(0, 1000)
    Message.objects.create(
        task_id=task_id,
        time=timezone.now(),
        message='Task {0}:\t{1}'.format(task_id, str(round(num, 2)))
    )
    task = Task.objects.get(id=task_id)
    task.status = 2
    task.save()


@shared_task
def stop_task(task_id):
    try:
        task = PeriodicTask.objects.get(name=task_id)
        task_obj = Task.objects.get(id=int(task.name))
        task_obj.status = 2
        task_obj.save()
        task.enabled = False
        task.save()
        task.delete()
    except ObjectDoesNotExist:
        print('Task not exist or already ended!')

