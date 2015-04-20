__author__ = 'sbr'

from django import forms
from multiupload.fields import MultiFileField

class MyUploadForm(forms.Form):
    attachments = MultiFileField(max_num=99, min_num=1, max_file_size=1024*1024*5,
                                 label="Select the files to upload")

