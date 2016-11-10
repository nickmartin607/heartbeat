import datetime, random, threading, time
from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone
from core.models import Model
from core.forms import Form
from .plugins import *


DEFAULT_CREDENTIALS = 'username:password'
PROTOCOLS = [
    'Active Directory', 'DNS', 'FTP', 'HTTP', 'NFS', 'SMB', 'MySQL', 'SSH',
    'Telnet',
]
OPERATING_SYSTEMS = [
    'Windows XP', 'Windows Vista', 'Windows 7', 'Windows 8', 'Windows 10',
    'Windows Server 2003', 'Windows Server 2008', 'Windows Server 2012',
    'Windows - Other', 'Ubuntu Linux', 'Kali Linux', 'CentOS Linux',
    'Linux - Other', 'Other',
]


################################################################################
# class Team
#       ForeignKey: Group
################################################################################
class Team(Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='teams', verbose_name="Group Account")
    name = models.CharField(max_length=30, verbose_name="Name")
    
    @property
    def uptime(self):
        service_uptimes = [s.uptime for s in self.service_set.filter(visible=True)]
        try:
            percentage = int(sum(service_uptimes) / float(len(service_uptimes)))
            return '{}%'.format(percentage)
        except:
            return 'N/A'
    @property
    def score(self):
        service_points = sum([s.points_earned for s in self.service_set.all()])
        task_points = sum([t.points_earned for t in self.task_set.all()])
        inject_points = sum([i.points_earned for i in self.inject_set.all()])
        return service_points + inject_points + task_points
    @property
    def color(self):
        group = str(self.group).lower()
        return group if group in ['blue', 'red'] else 'grey'
    
    def __str__(self):
        return self.name
    
    class Meta:
        permissions = [('view_team', 'Can view team')]
################################################################################
# class Objective[abstract]
#       ForeignKey: Team
################################################################################
class ScoringModel(Model):
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Team")
    status = models.BooleanField(default=False, verbose_name="Status")
    details = models.TextField(max_length=600, blank=True, null=True, verbose_name="Details")
    point_value = models.PositiveIntegerField(default=100, verbose_name="Point Value")
    points_earned = models.PositiveIntegerField(default=0, verbose_name="Points Earned")
    
    def earn(self):
        if self.visible:
            self.points_earned += self.point_value
            self.save()
    
    class Meta:
        abstract = True
################################################################################
# class ActionModel[abstract]
################################################################################
class ActionModel(ScoringModel):
    subject = models.CharField(max_length=100, verbose_name="Subject")
    completed = models.DateTimeField(blank=True, null=True, verbose_name="Date/Time Completed")
    
    def __str__(self):
        return self.subject
    def complete(self):
        if not self.status:
            self.earn()
            self.visible = False
            self.status = True
            self.completed = timezone.now()
            self.save()
            
    class Meta:
        abstract = True
################################################################################
# class Task <- ActionModel
################################################################################
class Task(ActionModel):
        
    class Meta:
        permissions = [('view_task', 'Can view task')]
################################################################################
# class Inject <- ActionModel
################################################################################
class Inject(ActionModel):
    available = models.DateTimeField(blank=True, null=True, verbose_name="Date/Time Available")
    deadline = models.DateTimeField(blank=True, null=True, verbose_name="Date/Time Deadline")
    
    def toggle(self):
        try:
            if not self.status and (not self.deadline or timezone.now() < self.deadline):
                super(Inject, self).toggle()
        except:
            pass
    @classmethod
    def run(cls):
        for inject in cls.objects.all():
            if inject.visible:
                if inject.deadline and timezone.now() > inject.deadline:
                    inject.toggle()
            else:
                if inject.available and timezone.now() > inject.available:
                    inject.toggle()
    
    class Meta:
        permissions = [('view_inject', 'Can view inject')]
class InjectForm(Form):
    redirect_url = 'inject:all'
    class Meta:
        model = Inject
        fields = ['team', 'subject', 'details', 'available', 'deadline', 'point_value']
################################################################################
# class Credential
################################################################################
class Credential(Model):
    name = models.CharField(max_length=40, verbose_name='System Description')
    username = models.CharField(max_length=20, default=DEFAULT_CREDENTIALS.split(':')[0], verbose_name='Username')
    password = models.CharField(max_length=40, default=DEFAULT_CREDENTIALS.split(':')[1], verbose_name='Password')
    
    def __str__(self):
        return '{} [{}:{}]'.format(self.name, self.username, self.password)

    class Meta:
        permissions = [('view_credential', 'Can view credential')]
################################################################################
# class Host <- ScoringModel
################################################################################
class Host(ScoringModel):
    ip = models.GenericIPAddressField(verbose_name="IP Address")
    name = models.CharField(max_length=40, blank=True, verbose_name="Host Description")
    hostname = models.CharField(max_length=40, blank=True, verbose_name="Hostname")
    os = models.CharField(max_length=80, blank=True, choices=[(p, p) for p in OPERATING_SYSTEMS], verbose_name="Operating System")
    last_checked = models.DateTimeField(blank=True, null=True, verbose_name="Last Checked")
    
    def __str__(self):
        return str(self.name)
    def do_check(self):
        if self.visible:
            check = Check(host=self)
            check.check_host()
        
    @property
    def base_os(self):
        if 'linux' in self.os.lower():
            return 'linux'
        elif 'windows' in self.os.lower():
            return 'windows'
        else:
            return 'other'
    
    class Meta:
        permissions = [('view_host', 'Can view host')]
class HostForm(Form):
    redirect_url = 'system:all'
    class Meta:
        model = Host
        fields = ['team', 'ip', 'name', 'hostname', 'os']
################################################################################
# class Service <- ScoringModel
#       ForeignKey: Host
################################################################################
class Service(ScoringModel):
    host = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='Host System')
    protocol = models.CharField(max_length=20, choices=[(p, p) for p in PROTOCOLS], verbose_name='Protocol')
    port = models.PositiveIntegerField(verbose_name='Port Number')
    expected_result = models.TextField(blank=True, verbose_name='Expected Results')
    last_checked = models.DateTimeField(blank=True, null=True, verbose_name="Last Checked")
    credential = models.OneToOneField(Credential, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Credential')

    def __str__(self):
        return '{}-{}'.format(self.protocol, self.host)
    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)
        try:
            self.team = self.host.team
            self.save()
        except:
            pass
    def save(self, *args, **kwargs):
        super(Service, self).save(*args, **kwargs)
        if not self.credential:
            credential = Credential(name=self)
            credential.save()
            self.credential = credential
            self.save()
    def do_check(self):
        if self.visible:
            check = Check(host=self.host, service=self)
            check.check_service()
    def earn(self):
        if self.visible:
            self.points_earned += self.point_value
            self.save()
        
    @property
    def check_count(self):
        return len(self.check_set.all())
    @property
    def checks_successful(self):
        return len(self.check_set.filter(status=True))
    @property
    def uptime(self):
        try:
            return int(float(self.checks_successful) / self.check_count * 100)
        except:
            return 0
    
    @classmethod
    def run(cls):
        for service in cls.objects.filter(visible=True).filter(team__visible=True):
            service.do_check()
        
    class Meta:
        permissions = [('view_service', 'Can view service')]
class ServiceForm(Form):
    redirect_url = 'system:all'
    class Meta:
        model = Service
        fields = ['host', 'protocol', 'port', 'point_value']
################################################################################
# class Schedule
#       References: Service, Inject
# get_schedule()
################################################################################
class Schedule(Model):
    period_fixed = models.PositiveIntegerField(default=60)
    period_min = models.PositiveIntegerField(default=5)
    period_max = models.PositiveIntegerField(default=15)
    
    def toggle(self):
        super(Schedule, self).toggle()
        if self.visible:
            t1 = threading.Thread(target=self.service_checks)
            t2 = threading.Thread(target=self.general_tasks)
            t1.start()
            t2.start()
    def service_checks(self):
        while True:
            time.sleep(random.randint(self.period_min, self.period_max))
            Service.run()
            self.refresh_from_db()
            if not self.visible:
                break
    def general_tasks(self):
        while True:
            time.sleep(self.period_fixed)
            Inject.run()
            self.refresh_from_db()
            if not self.visible:
                break
def get_schedule():
    try:
        return Schedule.objects.get(pk=1)
    except:
        schedule = Schedule(pk=1, visible=False)
        schedule.save()
        return schedule
################################################################################
# class Check <- ScoringModel
#       ForeignKey: Host, Service
################################################################################
class Check(ScoringModel):
    host = models.ForeignKey(Host, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Host')
    service = models.ForeignKey(Service, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Service')
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Timestamp")
    
    def __str__(self):
        return 'Host[{}], Service[{}]: {}'.format(
            self.host,
            self.service.protocol if self.service else 'N/A',
            'UP' if self.status else 'DOWN'
        )
    def __init__(self, *args, **kwargs):
        super(Check, self).__init__(*args, **kwargs)
        try:
            self.team = self.host.team
            self.save()
        except:
            pass
    def check_host(self, host_check_only=True):
        if self.host.base_os == 'windows':
            (status, details) = port_connect(ip=self.host.ip, port=135)
        else:
            (status, details) = ping(self.host)
        self.host.status = status
        self.host.last_checked = timezone.now()
        self.host.save()
        if host_check_only:
            self.status = status
            self.details = details
            self.save()
    def check_service(self):
        sixty_seconds_ago = timezone.now() - datetime.timedelta(seconds=60)
        if not self.service.last_checked or self.service.last_checked < sixty_seconds_ago:
            self.check_host(host_check_only=False)
        if self.host.status:
            try:
                (status, details) = plugins.get(self.service.protocol)(self)
            except:
                (status, details) = port_connect(ip=self.host.ip, port=self.service.port)
            self.service.status = status
            self.service.last_checked = timezone.now()
            self.service.save()
            if status:
                self.service.earn()
        else:
            (status, details) = (False, 'Host is Down, No Checks Performed')
        self.status = status
        self.details = details
        self.save()
    
    class Meta:
        permissions = [
            ('view_check', 'Can view check'),
            ('perform_check', 'Can perform check'),
        ]
        
        
