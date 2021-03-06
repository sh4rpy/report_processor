from django.contrib.auth import get_user_model
from django.forms import fields
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Task, Tag


class TasksTestViews(TestCase):
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

    def test_home_page_correct_context(self):
        """Шаблон главной страницы сформирован с правильным контекстом"""
        response = self.client.get(reverse('tasks_list'))
        task_name = response.context.get('tasks')[0].name
        task_description = response.context.get('tasks')[0].description
        task_company = response.context.get('tasks')[0].company
        self.assertEqual(task_name, 'test')
        self.assertEqual(task_description, 'test_desc')
        self.assertEqual(task_company, 'КП')

    def test_create_page_correct_context(self):
        """Шаблон добавление задачи сформирован с правильным контекстом"""
        response = self.client.get(reverse('create_task'))
        form_fields = {
            'date': fields.DateField,
            'tag': fields.ChoiceField,
            'name': fields.CharField,
            'description': fields.CharField,
            'company': fields.ChoiceField,
            'employees': fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_delete_task(self):
        """Проверяем, что задачи корректно удаляются"""
        self.client.delete(reverse('delete_task', kwargs={'pk': self.task.pk}))
        self.assertEqual(Task.objects.count(), 0)

    def test_filtering(self):
        """Тестирует фильтрацию по тегам на главной странице"""
        Tag.objects.bulk_create([
            Tag(name='tag'),
            Tag(name='tag2')
        ])
        Task.objects.bulk_create([
            Task(date='2021-01-01', tag=Tag.objects.first(), name='test', description='desc', company='КП'),
            Task(date='2021-01-01', tag=Tag.objects.last(), name='another_name', description='another_desc',
                 company='КП')
        ])
        response = self.client.get('/?tag=1')
        self.assertContains(response, 'test')
        self.assertNotContains(response, 'another_name')
