from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core import serializers
from django.utils import timezone
import json
import pytz
import datetime

from .forms import TaskForm
from .models import Task, Message
from . import tasks

task_type_dict = {0: '每天', 1: '每周', 2: '每月', 3: '一次'}
task_status_dict = {0: '待执行', 1: '正在执行', 2: '已结束'}


def indexView(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task_type = form.cleaned_data.get('task_type')
            if task_type == '3':
                tf = form.save()
                tasks.generate_num_once.apply_async(args=[tf.pk], eta=form.cleaned_data.get('start_date'))
            else:
                execute_time = form.cleaned_data.get('execute_time')
                week = form.cleaned_data.get('week')
                month_of_year = form.cleaned_data.get('month_of_year')
                day_of_month = form.cleaned_data.get('day_of_month')
                # create task a little earlier than start_time
                if execute_time == None or task_type == '1' and len(week) == 0 or task_type == '2' and (
                        len(month_of_year) == 0 or len(day_of_month) == 0):
                    print(form.cleaned_data)
                    messages.warning(request, '请填写完整')
                    form = TaskForm()
                    return render(request, 'task_mgmt/task.html', {'form': form})
                tf = form.save()
                tasks.schedule_periodic_task.apply_async(
                    args=[tf.pk, task_type, execute_time, week, month_of_year, day_of_month],
                    eta=form.cleaned_data.get('start_date') - datetime.timedelta(seconds=30)
                )
            messages.success(request, '任务创建成功')
            form = TaskForm()
    else:
        form = TaskForm()
    return render(request, 'task_mgmt/task.html', {'form': form})


def route(request):
    return redirect('dashboard')


def task_list(request):
    if request.method == 'GET':
        tasks = json.loads(serializers.serialize("json", Task.objects.all()))
        return HttpResponse(json.dumps(formalize_tasks(tasks)))


def formalize_tasks(task_list):
    result = []
    for task in task_list:
        task_dict = task['fields']
        task_dict['id'] = task['pk']

        task_dict['task_type'] = task_type_dict[task_dict['task_type']]
        task_dict['status'] = task_status_dict[task_dict['status']]
        task_dict['start_date'] = utc_to_local_time(task_dict['start_date'], '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d %H:%M')
        result.append(task_dict)
    result = sorted(result, key=lambda e: e.__getitem__('id'), reverse=True)
    return result


def msg_list(request):
    if request.method == 'GET':
        msgs = json.loads(serializers.serialize("json", Message.objects.all()))
        return HttpResponse(json.dumps(formalize_msgs(msgs)))


def formalize_msgs(msg_list):
    result = []
    for message in msg_list:
        msg_dict = message['fields']
        msg_dict['time'] = utc_to_local_time(msg_dict['time'][0:-5], '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S')
        result.append(msg_dict)
    result = sorted(result, key=lambda e: e.__getitem__('time'), reverse=True)
    return result


def utc_to_local_time(utc_time, input_pattern, output_pattern):
    utc = datetime.datetime.strptime(utc_time, input_pattern).replace(tzinfo=pytz.UTC)
    return utc.astimezone(timezone.get_current_timezone()).strftime(output_pattern)


def stop_task(request):
    if request.method == 'POST':
        tasks.stop_task(request.POST['id'])
        return HttpResponse(json.dumps({}))
