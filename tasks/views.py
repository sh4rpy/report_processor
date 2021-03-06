from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import TaskForm
from .models import Task, Tag
from .utils import filter_or_get_all_tasks


class TaskListView(LoginRequiredMixin, ListView):
    """Главная страница со списком выполненных задач"""
    template_name = 'index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tag = self.request.GET.get('tag')
        return Task.objects.select_related(
            'tag', 'employees').filter(filter_or_get_all_tasks(tag)).order_by('-date', '-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['index'] = True  # показываем фильтр по тегам только на главной
        context['current_tag_pk'] = self.request.GET.get('tag')
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    """Форма создания задачи"""
    form_class = TaskForm
    template_name = 'tasks/create_or_update_task.html'
    success_url = reverse_lazy('tasks_list')


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """Форма редактирования задачи"""
    form_class = TaskForm
    template_name = 'tasks/create_or_update_task.html'
    success_url = reverse_lazy('tasks_list')
    queryset = Task.objects.select_related('tag', 'employees')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True  # нужно для правильного рендеринга кнопки и заголовка
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление задачи"""
    model = Task
    success_url = reverse_lazy('tasks_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
