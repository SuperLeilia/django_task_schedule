# Generated by Django 3.2.9 on 2021-12-15 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_mgmt', '0005_alter_task_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='task',
            name='interval',
        ),
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.SmallIntegerField(choices=[(0, '每天'), (1, '每周'), (3, '每月'), (4, '一次')], default=0, verbose_name='希望任务多久执行一次？'),
        ),
    ]