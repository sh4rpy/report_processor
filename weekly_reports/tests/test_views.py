from django.forms import fields
from django.test import TestCase, Client
from django.urls import reverse


class WeeklyReportsTestViews(TestCase):
    def setUp(self):
        self.client = Client()

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
