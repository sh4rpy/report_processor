from django.forms import fields
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Task


class TaskTestViews(TestCase):
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

    def test_report_page_correct_context(self):
        """Шаблон скачивания отчета сформирован с правильным контекстом"""
        response = self.client.get(reverse('report'))
        form_fields = {
            'date_from': fields.DateField,
            'date_to': fields.DateField,
            'company': fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_search(self):
        Task.objects.bulk_create([
            Task(date='2021-01-01', name='test2', description='desc', company='КП'),
            Task(date='2021-01-01', name='another', description='another_desc', company='КП')
        ])
        response = self.client.get('/?query=test')
        self.assertContains(response, 'desc')
        self.assertContains(response, 'test')
        self.assertNotContains(response, 'another')
        self.assertNotContains(response, 'another_desc')
