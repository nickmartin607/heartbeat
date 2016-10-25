# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('user', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Name', max_length=30)),
                ('total_points', models.PositiveIntegerField(default=0, verbose_name='Points')),
                ('group', models.ForeignKey(verbose_name='Group Account', to='auth.Group')),
            ],
            options={
                'permissions': [('view_team', 'Can view team')],
            },
        ),
    ]
