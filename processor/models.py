from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тег')

    def __str__(self):
        return self.name


class Task(models.Model):
    class Meta:
        ordering = ['-pk']

    COMPANY_CHOICES = [
        ('КП', 'КП',),
        ('АО', 'АО',),
    ]
    EMPLOYEES_CHOICES = [
        ('Левашов/Шитик', 'Левашов/Шитик'),
        ('Фурсов/Дмитриев', 'Фурсов/Дмитриев'),
    ]
    date = models.DateField(verbose_name='Дата')
    tag = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')
    name = models.CharField(max_length=70, verbose_name='Название')
    description = models.TextField(verbose_name='Подробное описание задачи')
    company = models.CharField(max_length=2, verbose_name='Компания', choices=COMPANY_CHOICES)
    employees = models.CharField(max_length=15, verbose_name='Работники', choices=EMPLOYEES_CHOICES)

    def __str__(self):
        return self.name
