import datetime
from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone
from .plugins import *
from .tasks import *

OS_CHOICES = [
    'Windows XP', 'Windows Vista', 'Windows 7', 'Windows 8', 'Windows 10',
    'Windows Server 2003', 'Windows Server 2008', 'Windows Server 2012',
    'Windows - Other', 'Ubuntu Linux', 'Kali Linux', 'CentOS Linux',
    'Linux - Other', 'Other',
]
PROTOCOL_CHOICES = [
    'Active Directory', 'DNS', 'FTP', 'HTTP', 'NFS', 'SMB', 'MySQL', 'SSH',
    'Telnet',
]

#########################################################################################
# Configuration #########################################################################
class Configuration(models.Model):
    period_fixed = models.PositiveIntegerField(default=30)
    period_min = models.PositiveIntegerField(default=120)
    period_max = models.PositiveIntegerField(default=300)
    hosts_id = models.CharField(max_length=40, null=True, blank=True)
    services_id = models.CharField(max_length=40, null=True, blank=True)

def get_config():
    try:
        return Configuration.objects.get(pk=1)
    except:
        config = Configuration(pk=1)
        config.save()
        return config
# Configuration #########################################################################
#########################################################################################

#########################################################################################
# Common ################################################################################
class Team(models.Model):
    group = models.ForeignKey(Group,
        on_delete=models.CASCADE, verbose_name="Group Account")
    name = models.CharField(max_length=30, verbose_name="Name")
    
    @property
    def score(self):
        return sum([s.value for s in self.points_set.all()])
    @property
    def uptime(self):
        uptimes = [s.uptime for s in self.service_set.filter(visible=True)]
        if len(uptimes) > 0:
            return '{}%'.format(int(sum(uptimes) / float(len(uptimes))))
        return 'N/A'
    
    def __str__(self):
        return self.name
    
    class Meta:
        permissions = [('view_team', 'Can view team')]

class Points(models.Model):
    team = models.ForeignKey(Team,
        on_delete=models.CASCADE, verbose_name="Team")
    details = models.CharField(max_length=80, verbose_name="Details")
    value = models.PositiveIntegerField(
        default=0, verbose_name="Points Earned")
    timestamp = models.DateTimeField(
        default=timezone.now, verbose_name="Timestamp")
    
    def __str__(self):
        return '{}: {}[{}]'.format(self.value, self.details, self.timestamp)
# Common ################################################################################
#########################################################################################

#########################################################################################
# Abstract Models #######################################################################
class BaseModel(models.Model):
    team = models.ForeignKey(Team,
        on_delete=models.CASCADE, verbose_name="Team")
    visible = models.BooleanField(default=True, verbose_name="Visible?")
    
    def toggle(self):
        self.visible = not self.visible
        self.save()
    
    class Meta:
        abstract = True

class CheckedModel(models.Model):
    status = models.BooleanField(default=False, verbose_name="Status")
    last_checked = models.DateTimeField(
        blank=True, null=True, verbose_name="Last Checked")
        
    def execute_check(self, **kwargs):
        self.status = kwargs.get('result')
        self.last_checked = timezone.now()
        self.save()
        return (self.status, kwargs.get('details'))
    
    class Meta:
        abstract = True
        
class ScoredModel(BaseModel):
    point_value = models.PositiveIntegerField(
        default=100, verbose_name="Point Value")
        
    def earn(self):
        try:
            points = Points(team=self.team, value=self.point_value, details=self)
            points.save()
        except Exception as e:
            print(e)
        
    class Meta:
        abstract = True

class ActionModel(ScoredModel):
    details = models.TextField(max_length=600, verbose_name="Details")
    completed = models.BooleanField(default=False, verbose_name="Completed?")
    timestamp = models.DateTimeField(
        blank=True, null=True, verbose_name="Completion Timestamp")
    
    def complete(self):
        self.completed = True
        self.visible = False
        self.timestamp = timezone.now()
        self.save()
        self.earn()
    
    class Meta:
        abstract = True

class CheckModel(ScoredModel):
    result = models.BooleanField(default=False, verbose_name="Result")
    details = models.TextField(max_length=600, verbose_name="Details")
    timestamp = models.DateTimeField(
        default=timezone.now, verbose_name="Timestamp")
        
    def execute(self, **kwargs):
        self.result = kwargs.get('result')
        self.details = kwargs.get('details')
        self.point_value = kwargs.get('point_value')
        if not self.result:
            self.point_value = 0
        self.save()
        return (self.result, self.details)
    
    class Meta:
        abstract = True
# Abstract Models #######################################################################
#########################################################################################

#########################################################################################
# Classes ###############################################################################
class Host(BaseModel, CheckedModel):
    name = models.CharField(max_length=40, verbose_name="Host Description")
    ip = models.GenericIPAddressField(verbose_name="IP Address")
    hostname = models.CharField(max_length=80, blank=True,
        verbose_name="Hostname")
    os = models.CharField(max_length=80, blank=True,
        choices=[(i, i) for i in OS_CHOICES], verbose_name="Operating System")
    
    @property
    def base_os(self):
        if 'linux' in self.os.lower():
            return 'linux'
        elif 'windows' in self.os.lower():
            return 'windows'
        return 'other'

    def __str__(self):
        return str(self.name)
    def execute_check(self, **kwargs):
        check = HostCheck(host=self)
        (result, details) = check.execute()
        kwargs = {'result': result, 'details': details}
        return super(Host, self).execute_check(**kwargs)
    
    class Meta:
        permissions = [('view_host', 'Can view host')]

class Service(CheckedModel, ScoredModel):
    host = models.ForeignKey(Host,
        on_delete=models.CASCADE, verbose_name='Host System')
    protocol = models.CharField(
        max_length=20, choices=[(i, i) for i in PROTOCOL_CHOICES],
        verbose_name='Protocol')
    port = models.PositiveIntegerField(verbose_name='Port Number')
    username = models.CharField(
        max_length=20, default='username', verbose_name='Username')
    password = models.CharField(
        max_length=40, default='password', verbose_name='Password')
    expected_result = models.TextField(
        blank=True, verbose_name='Expected Results')
    notes = models.TextField(max_length=600, verbose_name="Notes")
    
    @property
    def uptime(self):
        checks = self.servicecheck_set.all()
        total_checks = len(checks)
        if total_checks > 0:
            successful_checks = float(len(checks.filter(result=True)))
            return int(successful_checks / total_checks * 100)
        return 0

    def __str__(self):
        return '{}:{}'.format(self.host, self.protocol)
    def execute_check(self, **kwargs):
        check = ServiceCheck(service=self)
        (result, details) = check.execute()
        if result:
            self.earn()
        kwargs = {'result': result, 'details': details}
        return super(Service, self).execute_check(**kwargs)
        
    class Meta:
        permissions = [('view_service', 'Can view service')]

class Inject(ActionModel):
    subject = models.CharField(max_length=120, verbose_name="Subject")
    available = models.DateTimeField(
        blank=True, null=True, verbose_name="Date/Time Available")
    deadline = models.DateTimeField(
        blank=True, null=True, verbose_name="Date/Time Deadline")
    
    def __str__(self):
        return self.subject
    def __init__(self, *args, **kwargs):
        super(Inject, self).__init__(*args, **kwargs)
        if not self.completed:
            now = timezone.now()
            try:
                if self.available < now and self.deadline > now:
                    self.visible = True
                else:
                    self.visible = False
                self.save()
            except:
                pass
    def toggle(self):
        try:
            if not self.deadline or timezone.now() < self.deadline:
                super(Inject, self).toggle()
        except:
            pass
    
    class Meta:
        permissions = [('view_inject', 'Can view inject')]

class Task(ActionModel):
    def __str__(self):
        return self.details
    class Meta:
        permissions = [('view_task', 'Can view task')]

class HostCheck(CheckModel):
    host = models.ForeignKey(Host,
        on_delete=models.CASCADE, verbose_name='Host')
    
    def __str__(self):
        return str(self.host)
    def __init__(self, *args, **kwargs):
        if 'host' in kwargs:
            kwargs['team'] = kwargs.get('host').team
        super(HostCheck, self).__init__(*args, **kwargs)
    def execute(self, **kwargs):
        (result, details) = ping(self.host.ip)
        kwargs = {'result': result, 'details': details, 'point_value': 0}
        return super(HostCheck, self).execute(**kwargs)
    
class ServiceCheck(CheckModel):
    service = models.ForeignKey(Service,
        on_delete=models.CASCADE, verbose_name='Service')
    
    def __str__(self):
        return str(self.service)
    def __init__(self, *args, **kwargs):
        if 'service' in kwargs:
            kwargs['team'] = kwargs.get('service').team
            kwargs['point_value'] = kwargs.get('service').point_value
        super(ServiceCheck, self).__init__(*args, **kwargs)
    def execute(self, **kwargs):
        (result, details) = port_connect(
            ip=self.service.host.ip,
            port=self.service.port
        )
        kwargs = {'result': result, 'details': details}
        return super(ServiceCheck, self).execute(**kwargs)
# Classes ###############################################################################
#########################################################################################

