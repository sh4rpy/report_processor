from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import TaskForm
from .models import Task, Tag


class TaskListView(ListView):
    """Главная страница со списком выполненных задач"""
    template_name = 'index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tag = self.request.GET.get('tag')
        if tag:
            return Task.objects.select_related(
                'tag', 'employees').filter(tag=tag).order_by('-date', '-pk')
        return Task.objects.select_related(
            'tag', 'employees').order_by('-date', '-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['index'] = True  # показываем фильтр по тегам только на главной
        return context


class TaskCreateView(CreateView):
    """Форма создания задачи"""
    form_class = TaskForm
    template_name = 'tasks/create_or_update_task.html'
    success_url = reverse_lazy('tasks_list')


class TaskUpdateView(UpdateView):
    """Форма редактирования задачи"""
    form_class = TaskForm
    template_name = 'tasks/create_or_update_task.html'
    success_url = reverse_lazy('tasks_list')
    queryset = Task.objects.select_related('tag', 'employees')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True  # нужно для правильного рендеринга кнопки и заголовка
        return context


class TaskDeleteView(DeleteView):
    """Удаление задачи"""
    model = Task
    success_url = reverse_lazy('tasks_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
