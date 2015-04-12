# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tandem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='dest_folder',
            field=models.CharField(default=b'data/tandemout', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='text_folder',
            field=models.CharField(default=b'data/tandemcorpus', max_length=200),
            preserve_default=True,
        ),
    ]
