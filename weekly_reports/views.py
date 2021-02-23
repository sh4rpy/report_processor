from django.urls import reverse_lazy
from django.views.generic import FormView

from tasks.models import Task
from weekly_reports.forms import WeeklyReportForm
from weekly_reports.utils import get_tasks_for_weekly_report, get_weekly_report_content, get_weekly_report


class WeeklyReportView(FormView):
    """Страница скачивания еженедельного отчета"""
    template_name = 'weekly_reports/weekly_report.html'
    form_class = WeeklyReportForm
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        super().form_valid(form)
        date_from = form.cleaned_data['date_from']
        date_to = form.cleaned_data['date_to']
        company = form.cleaned_data['company']
        tasks = get_tasks_for_weekly_report(Task, company, date_from, date_to)
        # создаем и отдаем отчет
        weekly_report = get_weekly_report(get_weekly_report_content(tasks, company, date_from, date_to))
        return weekly_report
