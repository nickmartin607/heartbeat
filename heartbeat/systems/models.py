from django.db import models
from core.models import Model
from heartbeat.teams.models import Team

DEFAULT_CREDENTIALS = ['username', 'password']
PROTOCOLS = ['Active Directory', 'DNS', 'FTP', 'HTTP', 'NFS', 'SMB', 'MySQL', 'SSH', 'Telnet']

class System(Model):
    status = models.BooleanField(default=False, verbose_name="Status")
    last_checked = models.DateTimeField(blank=True, null=True, verbose_name="Last Checked")
    notes = models.TextField(max_length=600, blank=True, verbose_name="Notes")
    
    def __init__(self, *args, **kwargs):
        kwargs['enabled'] = False
        super(System, self).__init__(*args, **kwargs)
    def toggle(self):
        self.enabled = not self.enabled
        self.save()
    
    class Meta:
        abstract = True
    
        
class Host(System):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='hosts', related_query_name='host', verbose_name="Team")
    ip = models.GenericIPAddressField(verbose_name="IP Address")
    name = models.CharField(max_length=40, blank=True, verbose_name="Host Description")
    hostname = models.CharField(max_length=40, blank=True, verbose_name="Hostname")
    os = models.CharField(max_length=80, blank=True, verbose_name="Operating System")
    
    def __str__(self):
        return str(self.name)
    def do_check(self):
        if self.enabled:
            from heartbeat.checks.models import Check
            check = Check(host=self)
            check.check_host()
    def is_windows(self):
        return 'windows' in self.os.lower()
    
    class Meta:
        permissions = [('view_host', 'Can view host')]


class Service(System):
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name='services', related_query_name='service', verbose_name="Host System")
    protocol = models.CharField(max_length=20, choices=[(p, p) for p in PROTOCOLS], verbose_name="Protocol")
    port = models.PositiveIntegerField(blank=True, null=True, verbose_name="Port Number")
    expected_result = models.TextField(blank=True, verbose_name="Expected Results")
    point_value = models.PositiveIntegerField(default=100, verbose_name="Point Value")
    uptime = models.PositiveIntegerField(default=0, verbose_name="Uptime")
    check_count = models.PositiveIntegerField(default=0, verbose_name="Total Checks")
    checks_successful = models.PositiveIntegerField(default=0, verbose_name="Total Successful Checks")

    def __str__(self):
        return '{}[{}]'.format(self.protocol, self.host)
    def save(self, *args, **kwargs):
        super(Service, self).save(*args, **kwargs)
        try:
            credential = Credential.objects.get(pk=self.id)
        except:
            credential = Credential(service=self)
            credential.save()
    def do_check(self):
        if self.enabled:
            from heartbeat.checks.models import Check
            check = Check(host=self.host, service=self)
            check.check_service()
    def update_stats(self, status):
        if status:
            self._get_team().adjust_points(self.point_value)
            self.checks_successful = int(self.checks_successful + 1)
        self.check_count = int(self.check_count + 1)
        self.uptime = int(float(self.checks_successful) / self.check_count * 100)
        self.save()
        
    @classmethod
    def schedule(cls):
        print("Checking Services!")
        for service in cls.objects.filter(enabled=True):
            if service._get_team().enabled:
                service.do_check()
        
    def _get_team(self):
        return self.host.team
    team = property(_get_team)
    
    class Meta:
        permissions = [('view_service', 'Can view service')]


class Credential(Model):
    service = models.OneToOneField(Service, primary_key=True, on_delete=models.CASCADE, verbose_name='Service')
    username = models.CharField(max_length=20, default=DEFAULT_CREDENTIALS[0], verbose_name="Username")
    password = models.CharField(max_length=40, default=DEFAULT_CREDENTIALS[1], verbose_name="Password")
    
    def __str__(self):
        return '{} [{}:{}]'.format(self.service, self.username, self.password)

    class Meta:
        permissions = [('view_credential', 'Can view credential')]


