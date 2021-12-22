from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
from datetime import datetime
import pytz


def create_periodic_task(task_id, task_location, task_type, execute_time, week, month_of_year, day_of_month):
    dt_dict = create_crontab(task_type, execute_time, week, month_of_year, day_of_month)
    print(dt_dict)
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=dt_dict['minute'],
        hour=dt_dict['hour'],
        day_of_week=dt_dict['day_of_week'],
        day_of_month=dt_dict['day_of_month'],
        month_of_year= dt_dict['month_of_year'],
        timezone=pytz.timezone('Asia/Shanghai')
    )

    PeriodicTask.objects.create(
        crontab=schedule,
        name=task_id,
        task=task_location,
        args=json.dumps([task_id]),  # parameters
    )


def list_to_str(item_list):
    result = ''
    for item in item_list:
        result += str(item) + ','
    return result[:-1]


def create_crontab(task_type, execute_time, week, month_of_year, day_of_month):
    result_dict = {'minute': '*', 'hour': '*', 'day_of_week': '*', 'day_of_month': '*', 'month_of_year': '*'}
    # Daliy
    exec_dt_obj = datetime.strptime(execute_time, '%H:%M:%S')
    result_dict['minute'] = str(exec_dt_obj.minute)
    result_dict['hour'] = str(exec_dt_obj.hour)
    # Weekly
    if task_type == '1':
        result_dict['day_of_week'] = list_to_str(week)
    # Monthly
    elif task_type == '2':
        result_dict['day_of_month'] = list_to_str(day_of_month)
        result_dict['month_of_year'] = list_to_str(month_of_year)
    return result_dict
