from django.db import models


class Tag(models.Model):
    """Модель для тегов"""
    name = models.CharField(max_length=50, verbose_name='Тег')

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Модель для работников"""
    employees = models.CharField(max_length=18, verbose_name='Работники')

    def __str__(self):
        return self.employees


class Task(models.Model):
    """Модель для задач"""
    class Meta:
        ordering = ['-date']

    COMPANY_CHOICES = [
        ('КП', 'КП',),
        ('АО', 'АО',),
    ]
    date = models.DateField(verbose_name='Дата')
    tag = models.ForeignKey(Tag, verbose_name='Тег', null=True, blank=True, on_delete=models.SET_NULL,
                            related_name='tasks')
    name = models.CharField(max_length=70, verbose_name='Название')
    description = models.TextField(verbose_name='Подробное описание задачи')
    company = models.CharField(max_length=2, verbose_name='Компания', choices=COMPANY_CHOICES)
    employees = models.ForeignKey(Employee, verbose_name='Работники', null=True, blank=True,
                                  on_delete=models.SET_NULL, related_name='tasks')

    def __str__(self):
        return self.name
