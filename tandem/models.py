
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


    def was_created_recently(self):
        return self.create_date >= timezone.now() - datetime.timedelta(days=1)

    was_created_recently.admin_order_field = 'create_date'
    was_created_recently.boolean = True
    was_created_recently.short_description = 'Created recently?'

class Infiles(models.Model):
    project_name = models.ForeignKey(Project)
    filename = models.CharField(max_length=200)

    def __unicode__(self):
        return self.filename



