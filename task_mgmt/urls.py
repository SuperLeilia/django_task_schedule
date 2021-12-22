from task_mgmt import views as task_views
from django.urls import path

urlpatterns = [
    path('', task_views.route),
    path('get_task_list', task_views.task_list),
    path('get_msg_list', task_views.msg_list),
    path('stop_task', task_views.stop_task),
    path('dashboard', task_views.indexView, name='dashboard'),
]