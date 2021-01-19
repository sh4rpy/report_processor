from django.http import HttpResponse
from docxtpl import DocxTemplate


def get_report_content(tasks, company, date_from, date_to):
    report_content = {
        'company': company,
        'date_from': date_from.strftime('%d.%m.%Y'),
        'date_to': date_to.strftime('%d.%m.%Y'),
        'tasks': [],
    }
    for task in tasks:
        report_content['tasks'].append(task.description)
    return report_content


def get_report(content):
    template = DocxTemplate('processor/docx/template.docx')
    template.render(content)
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=report.docx'
    template.save(response)
    return response
