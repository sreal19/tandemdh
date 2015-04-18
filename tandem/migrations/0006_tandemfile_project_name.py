# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tandem', '0005_auto_20150415_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='tandemfile',
            name='project_name',
            field=models.ForeignKey(default='0', to='tandem.Project'),
            preserve_default=False,
        ),
    ]
