from django.contrib import admin

from .models import Tag, Task


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date', 'tag', 'name', 'description', 'company', 'employees',)
    list_filter = ('date', 'company', 'employees',)
    search_fields = ('company', 'employees')
