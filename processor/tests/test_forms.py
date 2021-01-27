from django.test import TestCase, Client
from django.urls import reverse

from ..models import Task


class TaskTestForms(TestCase):
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

    def test_wrong_create_form_data(self):
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

    def test_generate_report(self):
        form_data = {
            'date_from': '2021-01-10',
            'date_to': '2021-01-10',
            'company': 'АО',
        }
        response = self.client.post(reverse('report'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename=report.docx')

    def test_wrong_data_generate_report(self):
        wrong_form_data = {
            'date_from': '2021-01-20',
            'date_to': '2021-01-10',
            'company': 'АО',
        }
        response = self.client.post(reverse('report'), data=wrong_form_data)
        self.assertFormError(response, 'form', 'date_from', 'Дата "От" не может быть больше даты "До"')
