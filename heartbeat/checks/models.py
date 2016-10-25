import datetime, socket, subprocess
from django.db import models
from django.utils import timezone
from core.models import Model
from heartbeat.systems.models import Host, Service
from .plugins import plugins


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
    def save(self, *args, **kwargs):
        self.description = kwargs.pop('description', 'N/A')
        self.status = kwargs.pop('status', False)
        super(Check, self).save(*args, **kwargs)
    def check_host(self, host_check_only=True):
        (status, message) = self.ping()
        self.host.status = status
        self.host.last_checked = timezone.now()
        self.host.save()
        if host_check_only:
            self.save(status=status, description=message)
    def check_service(self):
        sixty_seconds_ago = timezone.now() - datetime.timedelta(seconds=60)
        if not self.service.last_checked or self.service.last_checked < sixty_seconds_ago:
            self.check_host(host_check_only=False)
        if self.host.status:
            try:
                (status, message) = plugins.get(self.service.protocol)(self)
            except:
                (status, message) = self.port_connect()
            self.service.status = status
            self.service.last_checked = timezone.now()
            self.service.save()
            self.service.update_stats(status)
        else:
            (status, message) = (False, 'Host is Down, No Checks Performed')
        self.save(status=status, description=message)
    def ping(self, ping_count=1, ping_wait=1):
        if self.host.is_windows():
            return self.port_connect(port=135)
        else:
            cmd = ['ping', '-c', str(ping_count), '-w', str(ping_wait), self.host.ip]
            try:
                return_value = subprocess.check_call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if return_value == 0:
                    return (True, 'Ping Succeeded - Host is Alive')
                else:
                    return (False, 'Ping Succeeded - Host is Down')
            except Exception as e:
                return (False, 'Ping Failed - Error: "{}"'.format(e))
    
    def port_connect(self, port=None, timeout=5):
        try:
            port = port or self.service.port
            socket_pair = (self.host.ip, int(port))
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            return_value = sock.connect_ex(socket_pair)
            if return_value == 0:
                return (True, 'Port {} Connection Succeeded'.format(port))
            else:
                return (False, 'Port {} Connection Failed'.format(port))
        except Exception as e:
            return (False, 'Port Connection Failure - Error: "{}"'.format(e))
            
    class Meta:
        permissions = [
            ('view_check', 'Can view check'),
            ('perform_check', 'Can perform check'),
        ]

    
        
# DNS
# https://github.com/bplower/cssef/blob/refactor/plugins/cssefcdc/cssefcdc/plugins/DNS.py
# https://github.com/ubnetdef/scoreengine/blob/master/scoring/checks/dns.py

# FTP
# https://github.com/bplower/cssef/blob/refactor/plugins/cssefcdc/cssefcdc/plugins/FTP.py
# https://github.com/ubnetdef/scoreengine/blob/master/scoring/checks/ftp.py

# ICMP
# https://github.com/ubnetdef/scoreengine/blob/master/scoring/checks/imcp.py

# LDAP
# https://github.com/ubnetdef/scoreengine/blob/master/scoring/checks/ldap.py

# MySQL
# https://github.com/ubnetdef/scoreengine/blob/master/scoring/checks/mysql.py

# HTTP
# https://github.com/bplower/cssef/blob/refactor/plugins/cssefcdc/cssefcdc/plugins/HTTP.py
# https://github.com/ubnetdef/scoreengine/blob/master/scoring/checks/http.py

# SSH
# https://github.com/bplower/cssef/blob/refactor/plugins/cssefcdc/cssefcdc/plugins/SSH.py

# Open Port
# https://github.com/bplower/cssef/blob/refactor/plugins/cssefcdc/cssefcdc/plugins/OpenPort.py
