from django.http import HttpResponse
from docxtpl import DocxTemplate


def get_tasks_for_weekly_report(model_obj, company, date_from, date_to):
    """Отдает отфильтрованный кверисет с уникальными датой и описанием"""
    return model_obj.objects.select_related(
            'tag', 'employees').filter(
            date__gte=date_from).filter(
            date__lte=date_to).filter(
            company=company).order_by('date').values(
            'date', 'description').distinct()


def get_weekly_report_content(tasks, company, date_from, date_to):
    """Отдает контент для .docx файла"""
    report_content = {
        'company': company,
        'date_from': date_from.strftime('%d.%m.%Y'),
        'date_to': date_to.strftime('%d.%m.%Y'),
        'tasks': [f'- {task["date"].strftime("%d.%m.%Y")}. {task["description"]}' for task in tasks],
    }
    return report_content


def get_weekly_report(content):
    """Отдает пользователю готовый .docx файл"""
    template = DocxTemplate('weekly_reports/docx/template.docx')
    template.render(content)
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=weekly_report.docx'
    template.save(response)
    return response
