from django.forms import fields
from django.test import TestCase, Client
from django.urls import reverse

from tasks.models import Task


class WeeklyReportsTestViews(TestCase):
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

    def test_report_page_correct_context(self):
        """Шаблон скачивания отчета сформирован с правильным контекстом"""
        response = self.client.get(reverse('weekly_report'))
        form_fields = {
            'date_from': fields.DateField,
            'date_to': fields.DateField,
            'company': fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
