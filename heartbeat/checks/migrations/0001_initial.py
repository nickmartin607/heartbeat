# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('systems', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('timestamp', models.DateTimeField(null=True, auto_now_add=True, verbose_name='Timestamp')),
                ('description', models.CharField(blank=True, verbose_name='Description', max_length=100)),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('host', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checks', null=True, related_query_name='check', verbose_name='Host', to='systems.Host')),
                ('service', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checks', null=True, related_query_name='check', verbose_name='Service', to='systems.Service')),
            ],
            options={
                'permissions': [('view_check', 'Can view check'), ('perform_check', 'Can perform check')],
            },
        ),
    ]
