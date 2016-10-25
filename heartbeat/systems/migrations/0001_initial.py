# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('status', models.BooleanField(verbose_name='Status', default=False)),
                ('enabled', models.BooleanField(verbose_name='Enabled?', default=False)),
                ('last_checked', models.DateTimeField(verbose_name='Last Checked', blank=True, null=True)),
                ('ip', models.GenericIPAddressField(verbose_name='IP Address')),
                ('name', models.CharField(max_length=40, verbose_name='Host Description', blank=True)),
                ('hostname', models.CharField(max_length=40, verbose_name='Hostname', blank=True)),
                ('os', models.CharField(max_length=80, verbose_name='Operating System', blank=True)),
                ('notes', models.TextField(max_length=600, verbose_name='Notes', blank=True)),
                ('team', models.ForeignKey(related_name='hosts', related_query_name='host', to='teams.Team', verbose_name='Team')),
            ],
            options={
                'permissions': [('access_host', 'Can view host')],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('status', models.BooleanField(verbose_name='Status', default=False)),
                ('enabled', models.BooleanField(verbose_name='Enabled?', default=False)),
                ('last_checked', models.DateTimeField(verbose_name='Last Checked', blank=True, null=True)),
                ('protocol', models.CharField(max_length=20, verbose_name='Protocol', choices=[('Active Directory', 'Active Directory'), ('DNS', 'DNS'), ('FTP', 'FTP'), ('HTTP', 'HTTP'), ('NFS', 'NFS'), ('SMB', 'SMB'), ('MySQL', 'MySQL'), ('SSH', 'SSH'), ('Telnet', 'Telnet')])),
                ('port', models.PositiveIntegerField(verbose_name='Port Number', blank=True, null=True)),
                ('expected_result', models.TextField(verbose_name='Expected Results', blank=True)),
                ('point_value', models.PositiveIntegerField(verbose_name='Point Value', default=100)),
                ('uptime', models.PositiveIntegerField(verbose_name='Uptime', default=0)),
                ('check_count', models.PositiveIntegerField(verbose_name='Total Checks', default=0)),
                ('checks_successful', models.PositiveIntegerField(verbose_name='Total Successful Checks', default=0)),
            ],
            options={
                'permissions': [('view_service', 'Can view service')],
            },
        ),
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('service', models.OneToOneField(serialize=False, primary_key=True, verbose_name='Service', to='systems.Service')),
                ('username', models.CharField(max_length=20, verbose_name='Username', default='username')),
                ('password', models.CharField(max_length=40, verbose_name='Password', default='password')),
            ],
            options={
                'permissions': [('view_credential', 'Can view credential')],
            },
        ),
        migrations.AddField(
            model_name='service',
            name='host',
            field=models.ForeignKey(related_name='services', related_query_name='service', to='systems.Host', verbose_name='Host System'),
        ),
    ]
