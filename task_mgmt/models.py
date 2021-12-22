from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    task_type_choices = (
        (0, '每天'),
        (1, '每周'),
        (2, '每月'),
        (3, '一次'),
    )
    status_choices = (
        (0, '待执行'),
        (1, '正在执行'),
        (2, '已结束'),
    )
    title = models.CharField('任务名称', max_length=200, db_index=True)
    description = models.TextField('任务描述', max_length=200, blank=True)
    task_type = models.SmallIntegerField('希望任务多久执行一次？', default=0, choices=task_type_choices)
    start_date = models.DateTimeField('开始时间', null=True)
    execute_time = models.TimeField('何时执行？', null=True)
    status = models.SmallIntegerField('状态', default=0, choices=status_choices)
    week = models.CharField('周几执行？', max_length=500, blank=True)
    month_of_year = models.CharField('几月执行？', max_length=500, blank=True)
    day_of_month = models.CharField('每月几号执行？', max_length=500, blank=True)


class Message(models.Model):
    task_id = models.IntegerField()
    time = models.DateTimeField(null=True)
    message = models.CharField(max_length=500)
