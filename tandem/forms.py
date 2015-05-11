__author__ = 'sbr'

from django import forms
from django.forms import ModelForm
from fields import MultiFileField
from tandem.models import Project


class MyUploadForm(forms.Form):
    attachments = MultiFileField(max_num=130, min_num=1, max_file_size=1024*1024*100)
    class Media:
        css = {
            'all': ('{{ STATIC_URL }}css/TANDEMstyle.css',)
        }

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['project_name']



