from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from .forms import TaskForm, ReportForm
from .models import Task, Tag
from .utils import get_tasks, get_report_content, get_report


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
    template_name = 'processor/create_or_update_task.html'
    success_url = reverse_lazy('tasks_list')


class TaskUpdateView(UpdateView):
    """Форма редактирования задачи"""
    form_class = TaskForm
    template_name = 'processor/create_or_update_task.html'
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


class ReportView(FormView):
    """Страница создания отчета"""
    template_name = 'processor/report.html'
    form_class = ReportForm
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        super().form_valid(form)
        date_from = form.cleaned_data['date_from']
        date_to = form.cleaned_data['date_to']
        company = form.cleaned_data['company']
        tasks = get_tasks(Task, company, date_from, date_to)
        # создаем и отдаем отчет
        report = get_report(get_report_content(tasks, company, date_from, date_to))
        return report
