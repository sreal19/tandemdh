# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tandem', '0004_auto_20150411_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tandemfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tanfilename', models.CharField(max_length=200)),
                ('tanfiletype', models.CharField(max_length=10)),
                ('tanfile', models.FileField(upload_to=b'tandemin')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='infiles',
            name='project_name',
        ),
        migrations.DeleteModel(
            name='Infiles',
        ),
    ]
