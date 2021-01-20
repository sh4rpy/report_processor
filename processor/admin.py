from django.contrib import admin

from .models import Tag, Employee, Task


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employees',)
    list_filter = ('employees',)
    search_fields = ('employees',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date', 'tag', 'name', 'description', 'company', 'employees',)
    list_filter = ('date', 'company', 'employees',)
    search_fields = ('company', 'employees')
