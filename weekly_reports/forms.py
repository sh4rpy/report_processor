from django import forms

from tasks.models import Task


class WeeklyReportForm(forms.Form):
    """Форма создания отчета"""
    date_from = forms.DateField(widget=forms.DateInput(attrs={'class': 'input datetime-input', }), label='От:')
    date_to = forms.DateField(widget=forms.DateInput(attrs={'class': 'input datetime-input', }), label='До:')
    company = forms.ChoiceField(
        widget=forms.Select(), label='Компания', choices=Task.COMPANY_CHOICES
    )

    def clean(self):
        date_from = self.cleaned_data.get('date_from')
        date_to = self.cleaned_data.get('date_to')
        if date_from > date_to:
            self.add_error('date_from', 'Дата "От" не может быть больше даты "До"')
