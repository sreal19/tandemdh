# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tandem', '0002_auto_20150411_1126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='input_foler',
            new_name='input_fodler',
        ),
    ]
