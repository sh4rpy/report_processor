from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Task


class TasksTestForms(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Task.objects.create(
            date='2021-01-01',
            name='test',
            description='test_desc',
            company='КП',
        )

    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user('test', 'test@test.com', 'testpassword')
        self.client.force_login(self.user)
        self.task = Task.objects.get(name='test')

    def test_create_task(self):
        """Валидная форма создает новую запись в БД"""
        task_count = Task.objects.count()
        form_data = {
            'date': '2021-01-10',
            'name': 'test2',
            'description': 'test_desc2',
            'company': 'АО',
        }
        response = self.client.post(reverse('create_task'), data=form_data, follow=True)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertEqual(Task.objects.count(), task_count + 1)
        self.assertTrue(Task.objects.filter(name='test2').exists())

    def test_create_wrong_form_data(self):
        """Невалидная форма не создает запись в БД"""
        task_count = Task.objects.count()
        wrong_form_data = {
            'date': 'oooops',
            'name': 'test2',
            'description': 'test_desc2',
            'company': 'АО',
        }
        response = self.client.post(reverse('create_task'), data=wrong_form_data, follow=True)
        self.assertEqual(Task.objects.count(), task_count)
        self.assertFalse(Task.objects.filter(name='test2').exists())
        self.assertFormError(response, 'form', 'date', 'Введите правильную дату.')
