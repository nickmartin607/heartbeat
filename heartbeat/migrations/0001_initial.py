# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('visible', models.BooleanField(default=True, verbose_name='Visible?')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('details', models.TextField(max_length=600, null=True, verbose_name='Details', blank=True)),
                ('point_value', models.PositiveIntegerField(default=100, verbose_name='Point Value')),
                ('points_earned', models.PositiveIntegerField(default=0, verbose_name='Points Earned')),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', auto_now_add=True, null=True)),
            ],
            options={
                'permissions': [('view_check', 'Can view check'), ('perform_check', 'Can perform check')],
            },
        ),
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('visible', models.BooleanField(default=True, verbose_name='Visible?')),
                ('name', models.CharField(max_length=40, verbose_name='System Description')),
                ('username', models.CharField(default='username', max_length=20, verbose_name='Username')),
                ('password', models.CharField(default='password', max_length=40, verbose_name='Password')),
            ],
            options={
                'permissions': [('view_credential', 'Can view credential')],
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('visible', models.BooleanField(default=True, verbose_name='Visible?')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('details', models.TextField(max_length=600, null=True, verbose_name='Details', blank=True)),
                ('point_value', models.PositiveIntegerField(default=100, verbose_name='Point Value')),
                ('points_earned', models.PositiveIntegerField(default=0, verbose_name='Points Earned')),
                ('ip', models.GenericIPAddressField(verbose_name='IP Address')),
                ('name', models.CharField(max_length=40, verbose_name='Host Description', blank=True)),
                ('hostname', models.CharField(max_length=40, verbose_name='Hostname', blank=True)),
                ('os', models.CharField(verbose_name='Operating System', choices=[('Windows XP', 'Windows XP'), ('Windows Vista', 'Windows Vista'), ('Windows 7', 'Windows 7'), ('Windows 8', 'Windows 8'), ('Windows 10', 'Windows 10'), ('Windows Server 2003', 'Windows Server 2003'), ('Windows Server 2008', 'Windows Server 2008'), ('Windows Server 2012', 'Windows Server 2012'), ('Windows - Other', 'Windows - Other'), ('Ubuntu Linux', 'Ubuntu Linux'), ('Kali Linux', 'Kali Linux'), ('CentOS Linux', 'CentOS Linux'), ('Linux - Other', 'Linux - Other'), ('Other', 'Other')], max_length=80, blank=True)),
                ('last_checked', models.DateTimeField(verbose_name='Last Checked', null=True, blank=True)),
            ],
            options={
                'permissions': [('view_host', 'Can view host')],
            },
        ),
        migrations.CreateModel(
            name='Inject',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('visible', models.BooleanField(default=True, verbose_name='Visible?')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('details', models.TextField(max_length=600, null=True, verbose_name='Details', blank=True)),
                ('point_value', models.PositiveIntegerField(default=100, verbose_name='Point Value')),
                ('points_earned', models.PositiveIntegerField(default=0, verbose_name='Points Earned')),
                ('subject', models.CharField(max_length=100, verbose_name='Subject')),
                ('completed', models.DateTimeField(verbose_name='Date/Time Completed', null=True, blank=True)),
                ('available', models.DateTimeField(verbose_name='Date/Time Available', null=True, blank=True)),
                ('deadline', models.DateTimeField(verbose_name='Date/Time Deadline', null=True, blank=True)),
            ],
            options={
                'permissions': [('view_inject', 'Can view inject')],
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('visible', models.BooleanField(default=True, verbose_name='Visible?')),
                ('period_fixed', models.PositiveIntegerField(default=60)),
                ('period_min', models.PositiveIntegerField(default=5)),
                ('period_max', models.PositiveIntegerField(default=15)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('visible', models.BooleanField(default=True, verbose_name='Visible?')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('details', models.TextField(max_length=600, null=True, verbose_name='Details', blank=True)),
                ('point_value', models.PositiveIntegerField(default=100, verbose_name='Point Value')),
                ('points_earned', models.PositiveIntegerField(default=0, verbose_name='Points Earned')),
                ('protocol', models.CharField(verbose_name='Protocol', choices=[('Active Directory', 'Active Directory'), ('DNS', 'DNS'), ('FTP', 'FTP'), ('HTTP', 'HTTP'), ('NFS', 'NFS'), ('SMB', 'SMB'), ('MySQL', 'MySQL'), ('SSH', 'SSH'), ('Telnet', 'Telnet')], max_length=20)),
                ('port', models.PositiveIntegerField(verbose_name='Port Number')),
                ('expected_result', models.TextField(verbose_name='Expected Results', blank=True)),
                ('last_checked', models.DateTimeField(verbose_name='Last Checked', null=True, blank=True)),
                ('credential', models.OneToOneField(verbose_name='Credential', to='heartbeat.Credential', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('host', models.ForeignKey(verbose_name='Host System', to='heartbeat.Host')),
            ],
            options={
                'permissions': [('view_service', 'Can view service')],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('visible', models.BooleanField(default=True, verbose_name='Visible?')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('details', models.TextField(max_length=600, null=True, verbose_name='Details', blank=True)),
                ('point_value', models.PositiveIntegerField(default=100, verbose_name='Point Value')),
                ('points_earned', models.PositiveIntegerField(default=0, verbose_name='Points Earned')),
                ('subject', models.CharField(max_length=100, verbose_name='Subject')),
                ('completed', models.DateTimeField(verbose_name='Date/Time Completed', null=True, blank=True)),
            ],
            options={
                'permissions': [('view_task', 'Can view task')],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('visible', models.BooleanField(default=True, verbose_name='Visible?')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('group', models.ForeignKey(verbose_name='Group Account', related_name='teams', to='auth.Group')),
            ],
            options={
                'permissions': [('view_team', 'Can view team')],
            },
        ),
        migrations.AddField(
            model_name='task',
            name='team',
            field=models.ForeignKey(verbose_name='Team', to='heartbeat.Team', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='team',
            field=models.ForeignKey(verbose_name='Team', to='heartbeat.Team', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inject',
            name='team',
            field=models.ForeignKey(verbose_name='Team', to='heartbeat.Team', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='team',
            field=models.ForeignKey(verbose_name='Team', to='heartbeat.Team', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='check',
            name='host',
            field=models.ForeignKey(verbose_name='Host', to='heartbeat.Host', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='check',
            name='service',
            field=models.ForeignKey(verbose_name='Service', to='heartbeat.Service', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='check',
            name='team',
            field=models.ForeignKey(verbose_name='Team', to='heartbeat.Team', blank=True, null=True),
        ),
    ]
