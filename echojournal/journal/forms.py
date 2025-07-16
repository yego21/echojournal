from django import forms
from .models import JournalEntry
from datetime import date

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['date', 'start_entry', 'midday_entry', 'end_entry']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'start_entry': forms.Textarea(attrs={'rows': 2}),
            'midday_entry': forms.Textarea(attrs={'rows': 2}),
            'end_entry': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(JournalEntryForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = date.today()