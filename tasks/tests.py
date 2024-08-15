from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

class TaskTests(APITestCase):

    def setUp(self):
        # cria uma tarefa para ser testada
        self.task = Task.objects.create(
            title="Tarefa Teste",
            description="uma tarefa para teste",
            due_date="2024-08-18"
        )
        # procura o name declarado em urls.py
        self.url_create_list = reverse('task-create_list')

    def test_get_task(self):
        # testa a requisição GET para listar tarefas
        # verifica se a resposta retorna status 200 e se o titulo da tarefa confere
        response = self.client.get(self.url_create_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "Tarefa Teste")

    def test_create_task(self):
        # testa a requisição POST para criar uma nova tarefa
        # verifica se a resposta retorna status 201 e se a nova tarefa foi criada
        data = {
            "title": "Nova Tarefa Teste",
            "description": "Criando uma nova tarefa",
            "due_date": "2024-08-18"
        }
        response = self.client.post(self.url_create_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.last().title, "Nova Tarefa Teste")

