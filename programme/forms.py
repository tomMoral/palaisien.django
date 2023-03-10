from django import forms
from .models import Attendees


class SeminarRegistrationForm(forms.ModelForm):
    class Meta:
        model = Attendees
        fields = ['name', 'surname', 'institution', 'seminar']
        widgets = {'seminar': forms.HiddenInput()}
