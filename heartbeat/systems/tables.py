from core.tables import Table
from .models import Host, Service


class HostTable(Table):
    model = Host
    columns = [
        {'field': 'status', 'action': 'check', 'staff-only-action': True, 'styles': ['border-right', 'narrow']},
        {'field': 'team'},
        {'field': 'name', 'styles': ['border-right']},
        {'field': 'ip'},
        {'field': 'hostname'},
        {'field': 'os'},
        {'field': 'enabled', 'action': 'toggle', 'styles': ['border-left', 'narrow']},
        {'action': 'modify', 'styles': ['narrow']},
        {'action': 'delete', 'styles': ['narrow']},
    ]
   
    
class ServiceTable(Table):
    model = Service
    columns = [
        {'field': 'status', 'action': 'check', 'staff-only-action': True, 'styles': ['border-right', 'narrow']},
        {'field': 'host', 'staff-only': True},
        {'field': 'protocol'},
        {'field': 'port'},
        {'field': 'uptime', 'appended_text': '%'},
        {'field': 'enabled', 'action': 'toggle', 'styles': ['border-left', 'narrow'], 'staff-only': True},
        {'action': 'passwd', 'styles': ['narrow'], 'blue-only': True},
        {'action': 'modify', 'styles': ['narrow'], 'staff-only': True},
        {'action': 'delete', 'styles': ['narrow'], 'staff-only': True},
    ]


