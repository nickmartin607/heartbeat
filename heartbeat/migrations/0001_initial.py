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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('period_fixed', models.PositiveIntegerField(default=30)),
                ('period_min', models.PositiveIntegerField(default=120)),
                ('period_max', models.PositiveIntegerField(default=300)),
                ('hosts_id', models.CharField(blank=True, max_length=40, null=True)),
                ('services_id', models.CharField(blank=True, max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('visible', models.BooleanField(verbose_name='Visible?', default=True)),
                ('status', models.BooleanField(verbose_name='Status', default=False)),
                ('name', models.CharField(max_length=40, verbose_name='Host Description')),
                ('ip', models.GenericIPAddressField(verbose_name='IP Address')),
                ('hostname', models.CharField(blank=True, max_length=80, verbose_name='Hostname')),
                ('os', models.CharField(blank=True, choices=[('Windows XP', 'Windows XP'), ('Windows Vista', 'Windows Vista'), ('Windows 7', 'Windows 7'), ('Windows 8', 'Windows 8'), ('Windows 10', 'Windows 10'), ('Windows Server 2003', 'Windows Server 2003'), ('Windows Server 2008', 'Windows Server 2008'), ('Windows Server 2012', 'Windows Server 2012'), ('Windows - Other', 'Windows - Other'), ('Ubuntu Linux', 'Ubuntu Linux'), ('Kali Linux', 'Kali Linux'), ('CentOS Linux', 'CentOS Linux'), ('Linux - Other', 'Linux - Other'), ('Other', 'Other')], max_length=80, verbose_name='Operating System')),
            ],
            options={
                'permissions': [('view_host', 'Can view host')],
            },
        ),
        migrations.CreateModel(
            name='HostCheck',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('visible', models.BooleanField(verbose_name='Visible?', default=True)),
                ('point_value', models.PositiveIntegerField(verbose_name='Point Value', default=100)),
                ('result', models.BooleanField(verbose_name='Result', default=False)),
                ('details', models.TextField(max_length=600, verbose_name='Details')),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', default=django.utils.timezone.now)),
                ('host', models.ForeignKey(to='heartbeat.Host', verbose_name='Host')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Inject',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('visible', models.BooleanField(verbose_name='Visible?', default=True)),
                ('point_value', models.PositiveIntegerField(verbose_name='Point Value', default=100)),
                ('details', models.TextField(max_length=600, verbose_name='Details')),
                ('completed', models.BooleanField(verbose_name='Completed?', default=False)),
                ('timestamp', models.DateTimeField(blank=True, verbose_name='Completion Timestamp', null=True)),
                ('subject', models.CharField(max_length=120, verbose_name='Subject')),
                ('available', models.DateTimeField(blank=True, verbose_name='Date/Time Available', null=True)),
                ('deadline', models.DateTimeField(blank=True, verbose_name='Date/Time Deadline', null=True)),
            ],
            options={
                'permissions': [('view_inject', 'Can view inject')],
            },
        ),
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('details', models.CharField(max_length=80, verbose_name='Details')),
                ('value', models.PositiveIntegerField(verbose_name='Points Earned', default=0)),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('visible', models.BooleanField(verbose_name='Visible?', default=True)),
                ('status', models.BooleanField(verbose_name='Status', default=False)),
                ('point_value', models.PositiveIntegerField(verbose_name='Point Value', default=100)),
                ('protocol', models.CharField(choices=[('Active Directory', 'Active Directory'), ('DNS', 'DNS'), ('FTP', 'FTP'), ('HTTP', 'HTTP'), ('NFS', 'NFS'), ('SMB', 'SMB'), ('MySQL', 'MySQL'), ('SSH', 'SSH'), ('Telnet', 'Telnet')], max_length=20, verbose_name='Protocol')),
                ('port', models.PositiveIntegerField(verbose_name='Port Number')),
                ('username', models.CharField(verbose_name='Username', max_length=20, default='username')),
                ('password', models.CharField(verbose_name='Password', max_length=40, default='password')),
                ('expected_result', models.TextField(blank=True, verbose_name='Expected Results')),
                ('notes', models.TextField(max_length=600, verbose_name='Notes')),
                ('host', models.ForeignKey(to='heartbeat.Host', verbose_name='Host System')),
            ],
            options={
                'permissions': [('view_service', 'Can view service')],
            },
        ),
        migrations.CreateModel(
            name='ServiceCheck',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('visible', models.BooleanField(verbose_name='Visible?', default=True)),
                ('point_value', models.PositiveIntegerField(verbose_name='Point Value', default=100)),
                ('result', models.BooleanField(verbose_name='Result', default=False)),
                ('details', models.TextField(max_length=600, verbose_name='Details')),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', default=django.utils.timezone.now)),
                ('service', models.ForeignKey(to='heartbeat.Service', verbose_name='Service')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('visible', models.BooleanField(verbose_name='Visible?', default=True)),
                ('point_value', models.PositiveIntegerField(verbose_name='Point Value', default=100)),
                ('details', models.TextField(max_length=600, verbose_name='Details')),
                ('completed', models.BooleanField(verbose_name='Completed?', default=False)),
                ('timestamp', models.DateTimeField(blank=True, verbose_name='Completion Timestamp', null=True)),
            ],
            options={
                'permissions': [('view_task', 'Can view task')],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('group', models.ForeignKey(to='auth.Group', verbose_name='Group Account')),
            ],
            options={
                'permissions': [('view_team', 'Can view team')],
            },
        ),
        migrations.AddField(
            model_name='task',
            name='team',
            field=models.ForeignKey(to='heartbeat.Team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='servicecheck',
            name='team',
            field=models.ForeignKey(to='heartbeat.Team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='service',
            name='team',
            field=models.ForeignKey(to='heartbeat.Team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='points',
            name='team',
            field=models.ForeignKey(to='heartbeat.Team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='inject',
            name='team',
            field=models.ForeignKey(to='heartbeat.Team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='hostcheck',
            name='team',
            field=models.ForeignKey(to='heartbeat.Team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='host',
            name='team',
            field=models.ForeignKey(to='heartbeat.Team', verbose_name='Team'),
        ),
    ]
