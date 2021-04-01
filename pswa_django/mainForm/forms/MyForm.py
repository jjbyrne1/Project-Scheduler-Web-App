from django import forms
from .models.models import MyModel


class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ["fullname", "mobile_number", ]
        labels = {'fullname': "Name", "mobile_number": "Mobile Number", }