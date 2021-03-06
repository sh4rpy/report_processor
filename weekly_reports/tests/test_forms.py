from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class WeeklyReportsTestForms(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user('test', 'test@test.com', 'testpassword')
        self.client.force_login(self.user)

    def test_generate_weekly_report(self):
        """При валидной форме начинается скачивание еженедельного отчета"""
        form_data = {
            'date_from': '2021-01-10',
            'date_to': '2021-01-10',
            'company': 'АО',
        }
        response = self.client.post(reverse('weekly_report'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename=weekly_report.docx')

    def test_wrong_data_generate_weekly_report(self):
        """При невалидной форме скачивание еженедельного отчета не начинается"""
        wrong_form_data = {
            'date_from': '2021-01-20',
            'date_to': '2021-01-10',
            'company': 'АО',
        }
        response = self.client.post(reverse('weekly_report'), data=wrong_form_data)
        self.assertFormError(response, 'form', 'date_from', 'Дата "От" не может быть больше даты "До"')
