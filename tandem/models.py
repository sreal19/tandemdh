
from django.db import models
from django.utils import timezone
import datetime
from django import forms

class Project(models.Model):
    project_name = models.CharField(max_length=200)
    create_date = models.DateTimeField('date created')
    input_folder = models.CharField(max_length=200)
    dest_folder = models.CharField(max_length=200, default='data/tandemout')
    text_folder = models.CharField(max_length=200, default='data/tandemcorpus')

    def __str__(self):
        return self.project_name


class Tandemfile(models.Model):
    tanfilename = models.CharField(max_length=200)
    tanfiletype = models.CharField(max_length=10)
    tanfile = models.FileField(upload_to='/tandemin/')

    def __unicode__(self):
        return self.tanfilename



