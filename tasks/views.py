from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


def index(request):
    return HttpResponse('Sistema de Gerenciamento de Tarefas <br><br> Acesse a documentação no <a href="http://127.0.0.1:8000/docs">Swagger<a>')


# DOCUMENTAÇÃO SWAGGER PARA READ E CREATE TASKS
query_params = [
    openapi.Parameter('title', openapi.IN_QUERY, description='Título da tarefa', type=openapi.TYPE_STRING, required=False),
    openapi.Parameter('date', openapi.IN_QUERY, description='Data de vencimento', type=openapi.TYPE_STRING, required=False),
]


@swagger_auto_schema(
    method='get',
    operation_summary='Busca todas as tarefas',
    operation_description='Busca todas as tarefas que foram criadas. As tarefas marcadas como deletadas não aparecerão.',
    responses={200: TaskSerializer(many=True)},
    manual_parameters=query_params,
    security=[{'Bearer': []}],
)
@swagger_auto_schema(
    method='post',
    operation_summary='cria uma nova tarefa',
    operation_description='cria uma nova tarefa com os dados fornecidos na requisição',
    request_body=TaskSerializer,
    responses={201: TaskSerializer, 400: 'Requisição incorreta'},
    security=[{'Bearer': []}],
)
# VIEWS READ E CREATE TASKS
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def view_task(request):
    if request.method == 'GET':
        if request.query_params:
            title = request.query_params.get('title')
            due_date = request.query_params.get('date')

            if title and due_date:
                return Response({'error': 'Você deve passar um único parâmetro'}, status=status.HTTP_400_BAD_REQUEST)

            if title:
                tasks = Task.objects.filter(title__icontains=title, is_deleted=False)
            elif due_date:
                tasks = Task.objects.filter(due_date=due_date, is_deleted=False)
            else:
                return Response({'error': 'Parâmetro inválido'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)

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
    security=[{'Bearer': []}],
)
@swagger_auto_schema(
    method='put',
    operation_summary='atualiza tarefa por ID',
    operation_description='atualiza os campos de uma tarefa pelo seu ID',
    request_body=TaskSerializer,
    responses={200: TaskSerializer, 400: 'Requisição incorreta', 404: 'Tarefa não encontrada'},
    security=[{'Bearer': []}],
)
@swagger_auto_schema(
    method='delete',
    operation_summary='exclui tarefa',
    operation_description='oculta uma tarefa sem remove-la do banco de dados.',
    responses={200: 'Tarefa excluida', 404: 'Tarefa não encontrada'},
    security=[{'Bearer': []}],
)
# VIEWS READ BY ID, UPDATE E DELETE TASKS
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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
