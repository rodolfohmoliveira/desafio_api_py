from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Tarefa  # Adicione a importação do modelo Tarefa
from .serializers import TarefaSerializer  # Corrija a importação do serializer

class TarefaTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='12345')
        self.tarefa = Tarefa.objects.create(
            titulo='Teste Tarefa',
            descricao='Descrição da tarefa para teste.',
            autor='Autor do Teste',
            user=self.user
        )

    def test_str_representation(self):
        self.assertEqual(str(self.tarefa), 'Teste Tarefa')

    def test_titulo_max_length(self):
        max_length = self.tarefa._meta.get_field('titulo').max_length
        self.assertLessEqual(len(self.tarefa.titulo), max_length)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/atividades/tarefa/{}/'.format(self.tarefa.id))
        print(response.content.decode())  # Adicione esta linha
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('tarefa-view', args=[str(self.tarefa.id)]))
        print(response.content.decode())  # Adicione esta linha
        self.assertRedirects(response, '/accounts/login/?next={}'.format(reverse('tarefa-view', args=[str(self.tarefa.id)])), status_code=302)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('tarefa-view', args=[str(self.tarefa.id)]))
        print(response.content.decode())  # Adicione esta linha
        self.assertTemplateUsed(response, 'atividades/detail.html')
