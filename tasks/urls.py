from django.urls import path
from .views import view_tasks

urlpatterns = [
    path('', view_tasks)
]
