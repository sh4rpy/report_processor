from datetime import datetime

from django.test import TestCase

from tasks.models import Task, Tag
from ..utils import get_tasks_for_individual_report


class IndividualReportsTestUtils(TestCase):
    def setUp(self):
        Tag.objects.create(name='Test tag')
        Task.objects.bulk_create([
            Task(date=datetime.now(), name='test1', description='test_desc1', tag=Tag.objects.first()),
            Task(date=datetime.now(), name='test2', description='test_desc2', tag=Tag.objects.first())
        ])
        self.tasks = get_tasks_for_individual_report(Task, datetime.now(), datetime.now(), [1])

    def test_get_tasks_for_individual_report(self):
        """Проверяем, что отдаем нужный кверисет"""
        self.assertEqual(list(self.tasks), [(datetime.now().date(), 'test1', 'test_desc1'),
                                            (datetime.now().date(), 'test2', 'test_desc2')])
