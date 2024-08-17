from django.urls import path

from .views import detail_task, index, view_task

urlpatterns = [
    path('tasks/', view_task, name='task-create_list'),
    path('tasks/<int:id>', detail_task, name='task-detail'),
    path('', index, name='index'),
]
