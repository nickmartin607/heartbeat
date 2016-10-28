# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Enabled?'),
        ),
        migrations.AlterField(
            model_name='inject',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Enabled?'),
        ),
    ]
