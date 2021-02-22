from django.test import TestCase, Client
from django.urls import reverse

from tasks.models import Task


class WeeklyReportsTestForms(TestCase):
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

    def test_generate_report(self):
        """При валидной форме начинается скачивание отчета"""
        form_data = {
            'date_from': '2021-01-10',
            'date_to': '2021-01-10',
            'company': 'АО',
        }
        response = self.client.post(reverse('weekly_report'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename=report.docx')

    def test_wrong_data_generate_report(self):
        """При невалидной форме скачивание отчета не начинается"""
        wrong_form_data = {
            'date_from': '2021-01-20',
            'date_to': '2021-01-10',
            'company': 'АО',
        }
        response = self.client.post(reverse('weekly_report'), data=wrong_form_data)
        self.assertFormError(response, 'form', 'date_from', 'Дата "От" не может быть больше даты "До"')
