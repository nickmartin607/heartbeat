# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20161025_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='group',
            field=models.ForeignKey(to='auth.Group', related_name='teams', verbose_name='Group Account'),
        ),
    ]
