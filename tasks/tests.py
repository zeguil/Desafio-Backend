from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from .models import Task

# TESTES ENPOINTS READ E CREATE
class TaskTests(APITestCase):

    def setUp(self):
        # crie um usuario um token de acesso
        self.user = User.objects.create_user(username='user', password='password')
        self.token = RefreshToken.for_user(self.user)
        self.access_token = str(self.token.access_token)
        
        # cria tarefas para teste
        self.task1 = Task.objects.create(
            title="Tarefa 1",
            description="fazer compras",
            due_date="2024-09-20"
        )
        self.task2 = Task.objects.create(
            title="Tarefa 2",
            description="cria uma API",
            due_date="2024-10-19"
        )
        self.url_create_list = reverse('task-create_list')

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_get_task(self):
        # testa a requisição GET para listar tarefas
        # verifica se a resposta retorna status 200 e se o titulo da tarefa confere
        self.authenticate()
        response = self.client.get(self.url_create_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "Tarefa 1")

    def test_create_task(self):
        # testa a requisição POST para criar uma nova tarefa
        # verifica se a resposta retorna status 201 e se a nova tarefa foi criada
        data = {
            "title": "Nova Tarefa Teste",
            "description": "Criando uma nova tarefa",
            "due_date": "2024-08-30"
        }
        self.authenticate()
        response = self.client.post(self.url_create_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.last().title, "Nova Tarefa Teste")


# TESTES ENPOINTS READ BY ID, UPDATE E DELETE
class DetailTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.token = RefreshToken.for_user(self.user)
        self.access_token = str(self.token.access_token)

        self.task = Task.objects.create(
            title="update e delete",
            description="descricao de teste",
            due_date="2024-08-30"
        )
        self.detail_url = reverse('task-detail', args=[self.task.id])

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    

    def test_get_task(self):
        # testa a requisição GET por ID
        # verifica se retorna a terefa com id especifico e status 200
        self.authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)
        self.assertEqual(response.data['description'], self.task.description)

    def test_put_task(self):
        # testa a requisição PUT
        # verifica se retorna 200 e se os campos que foram atualizados
        self.authenticate()
        data = {
            "title": "tarefa atualizada",
            "description": "nova descricao",
            "due_date": "2024-08-30"
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, data['title'])
        self.assertEqual(self.task.description, data['description'])

    def test_delete_task(self):
        # testa a requisição DELETE
        # deleta uma tarefa, retorna status 200 e a menssagem
        self.authenticate()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Task deleted successfully.'})
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

# TESTS ENDPOINTS DE FILTRO POR TITULO E DATA
class TaskFilter(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.token = RefreshToken.for_user(self.user)
        self.access_token = str(self.token.access_token)

        self.task1 = Task.objects.create(
            title="Tarefa 1",
            description="fazer compras",
            due_date="2024-08-30"
        )
        self.task2 = Task.objects.create(
            title="Tarefa 2",
            description="cria uma API",
            due_date="2024-10-19"
        )
        self.url_create_list = reverse('task-create_list')

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    # teste de busca por titulo
    def test_get_task_by_title(self):
        self.authenticate()
        response = self.client.get(self.url_create_list, {'title': 'Tarefa 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], self.task1.title)

    #teste de busca por data
    def test_get_task_by_due_date(self):
        self.authenticate()
        response = self.client.get(self.url_create_list, {'date': '2024-10-19'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['due_date'], self.task2.due_date)
