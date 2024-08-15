from django.urls import path
from .views import view_task, detail_task

urlpatterns = [
    path('tasks', view_task, name='task-create_list'),
    path('tasks/<int:id>', detail_task, name='task-detail'),
]
