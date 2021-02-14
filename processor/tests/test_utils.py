from datetime import datetime

from django.test import TestCase

from ..models import Task
from ..utils import get_tasks, get_report_content


class TestUtils(TestCase):
    def setUp(self):
        Task.objects.bulk_create([
            Task(date=datetime.now(), name='test1', description='test_desc', company='КП'),
            Task(date=datetime.now(), name='test2', description='test_desc', company='КП')
        ])
        self.tasks = get_tasks(Task, 'КП', datetime.now(), datetime.now())

    def test_get_tasks(self):
        """Проверяем, что отдаем кверисет с уникальными датой и описанием"""
        self.assertEqual(len(self.tasks), 1)

    def test_get_report_content(self):
        """Тестирует функцию формирования контента для отчета"""
        report_content = get_report_content(self.tasks, 'КП', datetime.now(), datetime.now())
        expected = {
            'company': 'КП',
            'date_from': datetime.now().strftime('%d.%m.%Y'),
            'date_to': datetime.now().strftime('%d.%m.%Y'),
            'tasks': [f'- {datetime.now().strftime("%d.%m.%Y")}. test_desc'],
        }
        self.assertEqual(report_content, expected)
