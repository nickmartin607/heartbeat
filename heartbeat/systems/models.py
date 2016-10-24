from django.db import models
from core.models import Model
from heartbeat.teams.models import Team

DEFAULT_CREDENTIALS = ['username', 'password']
PROTOCOLS = ['Active Directory', 'DNS', 'FTP', 'HTTP', 'NFS', 'SMB', 'MySQL', 'SSH', 'Telnet']

class System(Model):
    status = models.BooleanField(default=False, verbose_name="Status")
    enabled = models.BooleanField(default=False, verbose_name="Enabled?")
    last_checked = models.DateTimeField(blank=True, null=True, verbose_name="Last Checked")

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
    notes = models.TextField(max_length=600, blank=True, verbose_name="Notes")
    
    def __str__(self):
        return str(self.name)
    def do_check(self):
        if self.enabled:
            from heartbeat.checks.models import Check
            check = Check(host=self)
            check.check_host()
    def is_windows(self):
        return 'windows' in self.os.lower()
    def can_view(self, user):
        if user.account._team() == self.team:
            if self.enabled:
                return True
        return False
    
    class Meta:
        permissions = [('access_host', 'Can Access Hosts')]


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
    def get_team(self):
        return self.host.team
    def do_check(self):
        if self.enabled:
            from heartbeat.checks.models import Check
            check = Check(service=self)
            status = check.check_service()
            if status in [True, False]:
                self.update_stats(status)
    def update_stats(self, status):
        if status:
            self.host.team.adjust_points(self.point_value)
            self.checks_successful = int(self.checks_successful + 1)
        self.check_count = int(self.check_count + 1)
        self.uptime = int(float(self.checks_successful) / self.check_count * 100)
        self.save()
    def can_view(self, user):
        if user.account._team() == self.host.team:
            if self.enabled:
                return True
        return False

    class Meta:
        permissions = [('access_service', 'Can Access Services')]


class Credential(Model):
    service = models.OneToOneField(Service, primary_key=True, on_delete=models.CASCADE, verbose_name='Service')
    username = models.CharField(max_length=20, default=DEFAULT_CREDENTIALS[0], verbose_name="Username")
    password = models.CharField(max_length=40, default=DEFAULT_CREDENTIALS[1], verbose_name="Password")
    
    def __str__(self):
        return '{} [{}:{}]'.format(self.service, self.username, self.password)
    def can_view(self, user):
        return self.service.can_view(user)

    class Meta:
        permissions = [('passwd_credential', 'Can Change Service Credentials')]
