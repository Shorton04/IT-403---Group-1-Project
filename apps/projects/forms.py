from django import forms

class ExampleForm(forms.Form):
    date_field = forms.DateField(input_formats=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"])
