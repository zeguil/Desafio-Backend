from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


# DOCUMENTAÇÃO SWAGGER PARA READ E CREATE TASKS
@swagger_auto_schema(
    method='get',
    operation_summary='busca todas as tarefas',
    operation_description='busca todas  as tarefas que foram criadas, as taferas marcadas como deletadas não irão aparecer',
    responses={
        200: TaskSerializer(many=True),
    },
)
@swagger_auto_schema(
    method='post',
    operation_summary='cria uma nova tarefa',
    operation_description='cria uma nova tarefa com os dados fornecidos na requisição',
    request_body=TaskSerializer,
    responses={201: TaskSerializer, 400: 'Requisição incorreta'},
)
# VIEWS READ E CREATE TASKS
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


# DOCUMENTAÇÃO SWAGGER PARA READ BY ID, UPDATE E DELETE TASKS
@swagger_auto_schema(
    method='get',
    operation_summary=' busca uma tarefa pelo seu ID',
    operation_description='busca uma tarefa pelo ID se ela não estiver marcada como deletada',
    responses={200: TaskSerializer, 404: 'Tarefa não encontrada'},
)
@swagger_auto_schema(
    method='put',
    operation_summary='atualiza tarefa por ID',
    operation_description='atualiza os campos de uma tarefa pelo seu ID',
    request_body=TaskSerializer,
    responses={200: TaskSerializer, 400: 'Requisição incorreta', 404: 'Tarefa não encontrada'},
)
@swagger_auto_schema(
    method='delete',
    operation_summary='exclui tarefa',
    operation_description='oculta uma tarefa sem remove-la do banco de dados.',
    responses={200: 'Tarefa excluida', 404: 'Tarefa não encontrada'},
)
# VIEWS READ BY ID, UPDATE E DELETE TASKS
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
