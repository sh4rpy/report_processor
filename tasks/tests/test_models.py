from django.test import TestCase

from ..models import Task


class TasksTestModels(TestCase):
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
        self.task = Task.objects.get(name='test')

    def test_verbose_name(self):
        """verbose_name полей соответствует ожиданиям"""
        fields_verbose_name = {
            'date': 'Дата',
            'tag': 'Тег',
            'name': 'Название',
            'description': 'Подробное описание задачи',
            'company': 'Компания',
            'employees': 'Работники',
        }
        for value, expected in fields_verbose_name.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.task._meta.get_field(value).verbose_name, expected
                )

    def test_object_name(self):
        """Метод __str__ возвращает название задачи"""
        self.assertEqual(str(self.task), self.task.name)
