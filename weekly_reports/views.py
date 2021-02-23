from django.urls import reverse_lazy
from django.views.generic import FormView

from tasks.models import Task
from weekly_reports.forms import WeeklyReportForm
from weekly_reports.utils import get_tasks, get_report_content, get_report


class WeeklyReportView(FormView):
    """Страница создания отчета"""
    template_name = 'weekly_reports/report.html'
    form_class = WeeklyReportForm
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
