# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systems', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='host',
            options={'permissions': [('view_host', 'Can view host')]},
        ),
        migrations.AddField(
            model_name='credential',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Enabled?'),
        ),
        migrations.AddField(
            model_name='service',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Notes', max_length=600),
        ),
        migrations.AlterField(
            model_name='host',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Enabled?'),
        ),
        migrations.AlterField(
            model_name='service',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Enabled?'),
        ),
    ]
