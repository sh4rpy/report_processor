from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from .forms import TaskForm, ReportForm
from .models import Task
from .utils import get_report_content, get_report


class TaskListView(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'


class TaskCreateView(CreateView):
    form_class = TaskForm
    template_name = 'create_or_update_task.html'
    success_url = reverse_lazy('tasks_list')


class TaskUpdateView(UpdateView):
    form_class = TaskForm
    template_name = 'create_or_update_task.html'
    success_url = reverse_lazy('tasks_list')
    queryset = Task.objects.all()


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ReportView(FormView):
    template_name = 'report.html'
    form_class = ReportForm
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        super().form_valid(form)
        date_from = form.cleaned_data['date_from']
        date_to = form.cleaned_data['date_to']
        company = form.cleaned_data['company']
        tasks = Task.objects.filter(
            date__gte=date_from).filter(
            date__lte=date_to).filter(
            company=company)
        report = get_report(get_report_content(tasks, company, date_from, date_to))
        return report
