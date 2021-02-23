from django.urls import reverse_lazy
from django.views.generic import FormView

from tasks.models import Task
from .forms import IndividualReportForm
from .utils import get_tasks_for_individual_report, get_individual_report


class IndividualReportView(FormView):
    """Страница скачивания индивидуального отчета"""
    template_name = 'individual_reports/individual_report.html'
    form_class = IndividualReportForm
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        super().form_valid(form)
        date_from = form.cleaned_data['date_from']
        date_to = form.cleaned_data['date_to']
        tags = form.cleaned_data['tags']
        tasks = get_tasks_for_individual_report(Task, date_from, date_to, tags)
        return get_individual_report(tasks)
