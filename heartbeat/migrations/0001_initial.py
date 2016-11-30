# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('period_fixed', models.PositiveIntegerField(default=30)),
                ('period_min', models.PositiveIntegerField(default=120)),
                ('period_max', models.PositiveIntegerField(default=300)),
                ('hosts_id', models.CharField(null=True, blank=True, max_length=40)),
                ('services_id', models.CharField(null=True, blank=True, max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('visible', models.BooleanField(verbose_name='Visible?', default=True)),
                ('status', models.BooleanField(verbose_name='Status', default=False)),
                ('last_checked', models.DateTimeField(verbose_name='Last Checked', null=True, blank=True)),
                ('name', models.CharField(verbose_name='Host Description', max_length=40)),
                ('ip', models.GenericIPAddressField(verbose_name='IP Address')),
                ('hostname', models.CharField(verbose_name='Hostname', blank=True, max_length=80)),
                ('os', models.CharField(max_length=80, verbose_name='Operating System', blank=True, choices=[('Windows XP', 'Windows XP'), ('Windows Vista', 'Windows Vista'), ('Windows 7', 'Windows 7'), ('Windows 8', 'Windows 8'), ('Windows 10', 'Windows 10'), ('Windows Server 2003', 'Windows Server 2003'), ('Windows Server 2008', 'Windows Server 2008'), ('Windows Server 2012', 'Windows Server 2012'), ('Windows - Other', 'Windows - Other'), ('Ubuntu Linux', 'Ubuntu Linux'), ('Kali Linux', 'Kali Linux'), ('CentOS Linux', 'CentOS Linux'), ('Linux - Other', 'Linux - Other'), ('Other', 'Other')])),
            ],
            options={
                'permissions': [('view_host', 'Can view host')],
            },
        ),
        migrations.CreateModel(
            name='HostCheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('visible', models.BooleanField(verbose_name='Visible?', default=True)),
                ('point_value', models.PositiveIntegerField(verbose_name='Point Value', default=100)),
                ('result', models.BooleanField(verbose_name='Result', default=False)),
                ('details', models.TextField(verbose_name='Details', max_length=600)),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', default=django.utils.timezone.now)),
                ('host', models.ForeignKey(verbose_name='Host', to='heartbeat.Host')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Inject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('visible', models.BooleanField(verbose_name='Visible?', default=True)),
                ('point_value', models.PositiveIntegerField(verbose_name='Point Value', default=100)),
                ('details', models.TextField(verbose_name='Details', max_length=600)),
                ('completed', models.BooleanField(verbose_name='Completed?', default=False)),
                ('timestamp', models.DateTimeField(verbose_name='Completion Timestamp', null=True, blank=True)),
                ('subject', models.CharField(verbose_name='Subject', max_length=120)),
                ('available', models.DateTimeField(verbose_name='Date/Time Available', null=True, blank=True)),
                ('deadline', models.DateTimeField(verbose_name='Date/Time Deadline', null=True, blank=True)),
            ],
            options={
                'permissions': [('view_inject', 'Can view inject')],
            },
        ),
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('details', models.CharField(verbose_name='Details', max_length=80)),
                ('value', models.PositiveIntegerField(verbose_name='Points Earned', default=0)),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('visible', models.BooleanField(verbose_name='Visible?', default=True)),
                ('status', models.BooleanField(verbose_name='Status', default=False)),
                ('last_checked', models.DateTimeField(verbose_name='Last Checked', null=True, blank=True)),
                ('point_value', models.PositiveIntegerField(verbose_name='Point Value', default=100)),
                ('protocol', models.CharField(verbose_name='Protocol', max_length=20, choices=[('Active Directory', 'Active Directory'), ('DNS', 'DNS'), ('FTP', 'FTP'), ('HTTP', 'HTTP'), ('NFS', 'NFS'), ('SMB', 'SMB'), ('MySQL', 'MySQL'), ('SSH', 'SSH'), ('Telnet', 'Telnet')])),
                ('port', models.PositiveIntegerField(verbose_name='Port Number')),
                ('username', models.CharField(verbose_name='Username', default='username', max_length=20)),
                ('password', models.CharField(verbose_name='Password', default='password', max_length=40)),
                ('expected_result', models.TextField(verbose_name='Expected Results', blank=True)),
                ('notes', models.TextField(verbose_name='Notes', max_length=600)),
                ('host', models.ForeignKey(verbose_name='Host System', to='heartbeat.Host')),
            ],
            options={
                'permissions': [('view_service', 'Can view service')],
            },
        ),
        migrations.CreateModel(
            name='ServiceCheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('visible', models.BooleanField(verbose_name='Visible?', default=True)),
                ('point_value', models.PositiveIntegerField(verbose_name='Point Value', default=100)),
                ('result', models.BooleanField(verbose_name='Result', default=False)),
                ('details', models.TextField(verbose_name='Details', max_length=600)),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', default=django.utils.timezone.now)),
                ('service', models.ForeignKey(verbose_name='Service', to='heartbeat.Service')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('visible', models.BooleanField(verbose_name='Visible?', default=True)),
                ('point_value', models.PositiveIntegerField(verbose_name='Point Value', default=100)),
                ('details', models.TextField(verbose_name='Details', max_length=600)),
                ('completed', models.BooleanField(verbose_name='Completed?', default=False)),
                ('timestamp', models.DateTimeField(verbose_name='Completion Timestamp', null=True, blank=True)),
            ],
            options={
                'permissions': [('view_task', 'Can view task')],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name', max_length=30)),
                ('group', models.ForeignKey(verbose_name='Group Account', to='auth.Group')),
            ],
            options={
                'permissions': [('view_team', 'Can view team')],
            },
        ),
        migrations.AddField(
            model_name='task',
            name='team',
            field=models.ForeignKey(verbose_name='Team', to='heartbeat.Team'),
        ),
        migrations.AddField(
            model_name='servicecheck',
            name='team',
            field=models.ForeignKey(verbose_name='Team', to='heartbeat.Team'),
        ),
        migrations.AddField(
            model_name='service',
            name='team',
            field=models.ForeignKey(verbose_name='Team', to='heartbeat.Team'),
        ),
        migrations.AddField(
            model_name='points',
            name='team',
            field=models.ForeignKey(verbose_name='Team', to='heartbeat.Team'),
        ),
        migrations.AddField(
            model_name='inject',
            name='team',
            field=models.ForeignKey(verbose_name='Team', to='heartbeat.Team'),
        ),
        migrations.AddField(
            model_name='hostcheck',
            name='team',
            field=models.ForeignKey(verbose_name='Team', to='heartbeat.Team'),
        ),
        migrations.AddField(
            model_name='host',
            name='team',
            field=models.ForeignKey(verbose_name='Team', to='heartbeat.Team'),
        ),
    ]
