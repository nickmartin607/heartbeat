# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20161025_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Enabled?'),
        ),
    ]
