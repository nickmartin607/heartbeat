# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='group',
            field=models.ForeignKey(related_name='team', to='auth.Group', verbose_name='Group Account'),
        ),
    ]
