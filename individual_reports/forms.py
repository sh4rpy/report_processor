from django import forms

from tasks.models import Tag


class IndividualReportForm(forms.Form):
    """Форма создания индивидуального отчета"""
    date_from = forms.DateField(widget=forms.DateInput(attrs={'class': 'input datetime-input', }), label='От:')
    date_to = forms.DateField(widget=forms.DateInput(attrs={'class': 'input datetime-input', }), label='До:')
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), label='Теги',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'})
    )

    def clean(self):
        date_from = self.cleaned_data.get('date_from')
        date_to = self.cleaned_data.get('date_to')
        if date_from > date_to:
            self.add_error('date_from', 'Дата "От" не может быть больше даты "До"')
