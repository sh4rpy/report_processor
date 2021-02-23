from django.shortcuts import reverse
from django.test import TestCase, Client

from ..models import Task


class TasksTestUrls(TestCase):
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

    def test_availability_of_all_pages(self):
        """Проверяет доступность всех страниц"""
        urls = {
            '/': reverse('tasks_list'),
            'new-task': reverse('create_task'),
            'update-task': reverse('update_task', kwargs={'pk': self.task.pk}),
            'delete-task': reverse('delete_task', kwargs={'pk': self.task.pk}),
        }
        for url, reverse_name in urls.items():
            with self.subTest(url=url):
                response = self.client.get(reverse_name)
                self.assertEqual(response.status_code, 302 if url == 'delete-task' else 200)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответсвующий шаблон"""
        templates_url_names = {
            reverse('tasks_list'): 'index.html',
            reverse('create_task'): 'tasks/create_or_update_task.html',
            reverse('update_task', kwargs={'pk': self.task.pk}): 'tasks/create_or_update_task.html',
        }
        for reverse_name, template in templates_url_names.items():
            with self.subTest(template=template):
                response = self.client.get(reverse_name)
                self.assertTemplateUsed(response, template)
