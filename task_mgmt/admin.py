from django.contrib import admin
from .models import Task, Message

admin.site.register(Task)
admin.site.register(Message)