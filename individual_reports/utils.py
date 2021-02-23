import csv

from django.http import HttpResponse


def get_tasks_for_individual_report(model_obj, date_from, date_to, tags):
    """Отдает отфильтрованный кверисет с задачами"""
    return model_obj.objects.select_related(
        'tag', 'employees').filter(
        date__gte=date_from).filter(
        date__lte=date_to).filter(
        tag__in=tags).order_by('date').values_list('date', 'name', 'description')


def get_individual_report(tasks):
    """Отдает готовый отчет в формате csv"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=individual_report.csv'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['Дата', 'Название задачи', 'Описание задачи'])
    writer.writerows(tasks)
    return response
