# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tandem', '0006_tandemfile_project_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tandemfile',
            name='project_name',
        ),
        migrations.DeleteModel(
            name='Tandemfile',
        ),
    ]
