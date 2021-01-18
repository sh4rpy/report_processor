from django import forms
from django.core.exceptions import ValidationError

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('date', 'tag', 'name', 'description', 'company', 'employees')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'input', }),
            'name': forms.TextInput(attrs={'class': 'input', }),
            'description': forms.Textarea(attrs={'class': 'textarea', }),
        }


class ReportForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'class': 'input', }), label='От:')
    date_to = forms.DateField(widget=forms.DateInput(attrs={'class': 'input', }), label='До:')
    company = forms.ChoiceField(
        widget=forms.Select(), label='Компания', choices=Task.COMPANY_CHOICES
    )

    def clean(self):
        date_from = self.cleaned_data.get('date_from')
        date_to = self.cleaned_data.get('date_to')
        if isinstance(date_from, type(None)) or isinstance(date_to, type(None)):
            raise ValidationError('')
        if date_from > date_to:
            raise ValidationError('Дата "От" не может быть больше даты "До"')
