from django.shortcuts import reverse
from django.test import TestCase, Client


class WeeklyReportsTestUrls(TestCase):
    def setUp(self):
        self.client = Client()

    def test_availability_weekly_report_page(self):
        """Проверяет доступность страницы формирования еженедельного отчета"""
        response = self.client.get(reverse('weekly_report'))
        self.assertEqual(response.status_code, 200)

    def test_weekly_report_url_uses_correct_template(self):
        """URL-адрес использует соответсвующий шаблон"""
        response = self.client.get(reverse('weekly_report'))
        self.assertTemplateUsed(response, 'weekly_reports/weekly_report.html')
