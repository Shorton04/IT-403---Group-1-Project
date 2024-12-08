from django import forms
from .models import SharedFile

class SharedFileForm(forms.ModelForm):
    class Meta:
        model = SharedFile
        fields = ['file', 'description']