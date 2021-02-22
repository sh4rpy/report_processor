from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    """Форма добавления/редактирования задачи"""
    class Meta:
        model = Task
        fields = ('date', 'tag', 'name', 'description', 'company', 'employees')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'input datetime-input', }),
            'name': forms.TextInput(attrs={'class': 'input', }),
            'description': forms.Textarea(attrs={'class': 'textarea', }),
        }
