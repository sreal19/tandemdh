__author__ = 'sbr'
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from tandem.models import Project, Infiles

class UploadFileForm(forms.Form):
#    title = forms.CharField(max_length=50)
    project = forms.CharField(label="Project Name", max_length=25)
#    folder = forms.CharField(label="Folder containing image files", max_length=100)
#    file  = forms.FileField()

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'create_date', 'input_folder', 'text_folder', 'dest_folder']

#create a form to add a Project
form = ProjectForm()
# Creating a form to change an existing Project
project = Project.objects.get(pk=1)
form = ProjectForm(instance=project)
