from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer

# READ E CREATE TASKS
@api_view(['GET', 'POST'])
def view_task(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(is_deleted=False)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# READ BY ID, UPDATE E DELETE TASKS
@api_view(['GET', 'PUT', 'DELETE'])
def detail_task(request, id):
    task = get_object_or_404(Task, pk=id, is_deleted=False)
    
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        task.is_deleted = True
        task.delete()
        return Response({'message': 'Task deleted successfully.'}, status=status.HTTP_200_OK)