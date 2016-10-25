# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='Subject')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('point_value', models.PositiveIntegerField(default=100, verbose_name='Point Value')),
                ('completed', models.DateTimeField(blank=True, null=True, verbose_name='Completed')),
                ('team', models.ForeignKey(to='teams.Team', verbose_name='Team')),
            ],
            options={
                'permissions': [('view_action', 'Can view action')],
            },
        ),
        migrations.CreateModel(
            name='Inject',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='Subject')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('point_value', models.PositiveIntegerField(default=100, verbose_name='Point Value')),
                ('completed', models.DateTimeField(blank=True, null=True, verbose_name='Completed')),
                ('details', models.TextField(max_length=600, verbose_name='Details')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled?')),
                ('available', models.DateTimeField(blank=True, null=True, verbose_name='Available')),
                ('deadline', models.DateTimeField(blank=True, null=True, verbose_name='Deadline')),
                ('team', models.ForeignKey(to='teams.Team', verbose_name='Team')),
            ],
            options={
                'permissions': [('view_inject', 'Can view inject')],
            },
        ),
    ]
