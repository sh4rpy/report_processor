from django.shortcuts import reverse
from django.test import TestCase, Client


class IndividualReportsTestUrls(TestCase):
    def setUp(self):
        self.client = Client()

    def test_availability_individual_report_page(self):
        """Проверяет доступность страницы формирования индивидуального отчета"""
        response = self.client.get(reverse('individual_report'))
        self.assertEqual(response.status_code, 200)

    def test_individual_report_url_uses_correct_template(self):
        """URL-адрес использует соответсвующий шаблон"""
        response = self.client.get(reverse('individual_report'))
        self.assertTemplateUsed(response, 'individual_reports/individual_report.html')
