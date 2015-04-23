
from django.db import models

class Project(models.Model):
    project_name = models.CharField(max_length=200, verbose_name="project:")
    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    input_folder = models.CharField(max_length=200, blank=True)
    dest_folder = models.CharField(max_length=200, blank=True)
    text_folder = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.project_name


class Tandemfile(models.Model):
    tanfilename = models.CharField(max_length=200)
    tanfiletype = models.CharField(max_length=10)
    tanfile = models.FileField(upload_to='/tandemin/')

    def __unicode__(self):
        return self.tanfilename



