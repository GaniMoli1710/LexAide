# forms.py in analysis app
# lawapp/forms.py
from django import forms
from .models import UploadedDocument

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedDocument
        fields = ['document', 'name']
