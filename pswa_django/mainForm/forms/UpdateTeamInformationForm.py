from django import forms
from .models.models import UpdateTeamInformation


class UpdateTeamInformationForm(forms.ModelForm):
    class Meta:
        model = UpdateTeamInformation
        fields = ["name", "advisor", "topic", ]
        labels = {'name': "Name", "advisor": "Advisor", "topic": "Topic", }