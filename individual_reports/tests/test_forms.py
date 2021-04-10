from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from tasks.models import Tag


class IndividualReportsTestForms(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user('test', 'test@test.com', 'testpassword')
        self.client.force_login(self.user)
        Tag.objects.create(name='Test tag')

    def test_generate_individual_report(self):
        """При валидной форме начинается скачивание индивидуального отчета"""
        form_data = {
            'date_from': '2021-01-10',
            'date_to': '2021-01-10',
            'tags': [1],
        }
        response = self.client.post(reverse('individual_report'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename=individual_report.csv')

    def test_wrong_date_generate_individual_report(self):
        """При невалидной дате скачивание индивидуального отчета не начинается"""
        wrong_form_data = {
            'date_from': '2021-01-20',
            'date_to': '2021-01-10',
            'tags': [1],
        }
        response = self.client.post(reverse('individual_report'), data=wrong_form_data)
        self.assertFormError(response, 'form', 'date_from', 'Дата "От" не может быть больше даты "До"')

    def test_wrong_tags_generate_individual_report(self):
        """При невалидных тегах скачивание индивидуального отчета не начинается"""
        wrong_form_data = {
            'date_from': '2021-01-20',
            'date_to': '2021-01-23',
            'tags': [],
        }
        response = self.client.post(reverse('individual_report'), data=wrong_form_data)
        self.assertFormError(response, 'form', 'tags', 'Обязательное поле.')
