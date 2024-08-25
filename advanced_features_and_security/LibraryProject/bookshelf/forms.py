from django import forms
from .models import ExampleModel  # Make sure to import your model

class ExampleForm(forms.ModelForm):
    class Meta:
        model = ExampleModel
        fields = ['field1', 'field2', 'field3']  # Replace with your actual fields