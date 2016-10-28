import datetime
from django.db import models
from django.utils import timezone
from core.models import Model
from heartbeat.systems.models import Host, Service
from .plugins import plugins, ping, port_connect


class Check(Model):
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Timestamp")
    description = models.CharField(max_length=100, blank=True, verbose_name="Description")
    status = models.BooleanField(default=False, verbose_name="Status")
    host = models.ForeignKey(Host, blank=True, null=True, on_delete=models.SET_NULL, related_name='checks', related_query_name='check', verbose_name='Host')
    service = models.ForeignKey(Service, blank=True, null=True, on_delete=models.SET_NULL, related_name='checks', related_query_name='check', verbose_name='Service')
    
    def __str__(self):
        service = self.service.protocol if self.service else 'N/A'
        status = 1 if self.status else 0
        return 'Check:{}  ->  Host[{}], Service[{}]'.format(str(status), self.host, service)
    def __init__(self, *args, **kwargs):
        super(Check, self).__init__(*args, **kwargs)
        if self.service:
            self.host = self.service.host
            self.save()
            self.check_service()
        else:
            self.check_host()
        
    def check_host(self, host_check_only=True):
        if self.host.is_windows():
            (status, message) = port_connect(host=self.host, port=135)
        else:
            (status, message) = ping(self.host)
        self.host.status = status
        self.host.last_checked = timezone.now()
        self.host.save()
        if host_check_only:
            self.status = status
            self.description = message
            self.save()
    def check_service(self):
        sixty_seconds_ago = timezone.now() - datetime.timedelta(seconds=60)
        if not self.service.last_checked or self.service.last_checked < sixty_seconds_ago:
            self.check_host(host_check_only=False)
        if self.host.status:
            try:
                (status, message) = plugins.get(self.service.protocol)(self)
            except:
                (status, message) = port_connect(ip=self.host.ip, port=self.service.port)
            self.service.status = status
            self.service.last_checked = timezone.now()
            self.service.save()
            self.service.update_stats(status)
        else:
            (status, message) = (False, 'Host is Down, No Checks Performed')
        self.status = status
        self.description = message
        self.save()
        return status
            
    class Meta:
        permissions = [
            ('view_check', 'Can view check'),
            ('perform_check', 'Can perform check'),
        ]