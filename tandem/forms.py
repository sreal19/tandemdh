__author__ = 'sbr'
from django import forms
from django.core.exceptions import ValidationError
from tandem.models import Infiles

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()

