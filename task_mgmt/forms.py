from django import forms
from django.utils import timezone
from .models import Task


def present_or_future_date(value):
    if value < timezone.now():
        raise forms.ValidationError("不能选择过去的时间")


class TaskForm(forms.ModelForm):
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
    week_choices = (
        (0, '周一'),
        (1, '周二'),
        (2, '周三'),
        (3, '周四'),
        (4, '周五'),
        (5, '周六'),
        (6, '周日'),
    )
    month_of_year_choices = (
        (1, '一月'),
        (2, '二月'),
        (3, '三月'),
        (4, '四月'),
        (5, '五月'),
        (6, '六月'),
        (7, '七月'),
        (8, '八月'),
        (9, '九月'),
        (10, '十月'),
        (11, '十一月'),
        (12, '十二月'),
    )
    day_of_month_choices = ((i, i) for i in range(1, 32))

    task_type = forms.ChoiceField(label='希望任务多久执行一次？', widget=forms.Select(), choices=task_type_choices,
                                  initial=task_type_choices[0])
    description = forms.Textarea(attrs={'style': 'height: 100px;'})
    start_date = forms.DateTimeField(
        label='开始时间',
        error_messages={
            'invalid': '日期不正确'
        },
        help_text='<ul>'
                  '<li>输入时间应晚于当前时间</li>'
                  '</ul>',
        validators=[present_or_future_date]
    )
    execute_time = forms.TimeField(label='何时执行？', required=False)
    status = forms.ChoiceField(label='状态', widget=forms.HiddenInput(), choices=status_choices,
                               initial=status_choices[0][0])
    week = forms.MultipleChoiceField(label='周几执行？', widget=forms.CheckboxSelectMultiple,
                                     choices=week_choices, required=False)
    month_of_year = forms.MultipleChoiceField(label='几月执行？', widget=forms.CheckboxSelectMultiple,
                                              choices=month_of_year_choices, required=False)
    day_of_month = forms.MultipleChoiceField(label='每月几号执行？', widget=forms.CheckboxSelectMultiple,
                                             choices=day_of_month_choices, required=False)

    class Meta:
        model = Task
        exclude = ()
