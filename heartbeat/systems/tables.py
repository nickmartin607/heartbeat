from core.tables import Table
from .models import Host, Service


class HostTable(Table):
    model = Host
    columns = [
        {'field': 'status',         'permission': 'view',       'styles': ['narrow', 'border-right']},
        {'field': 'team',           'permission': 'view'},
        {'field': 'name',           'permission': 'view',       'styles': ['border-right']},
        {'field': 'ip',             'permission': 'view'},
        {'field': 'hostname',       'permission': 'view'},
        {'field': 'os',             'permission': 'view'},
        {'field': 'enabled',        'permission': 'modify',     'action': 'toggle',     'styles': ['narrow', 'border-left']},
        {'common_action': 'check',  'permission': 'modify'},
        {'common_action': 'modify', 'permission': 'modify'},
        {'common_action': 'delete', 'permission': 'delete'},
    ]
   
    
class ServiceTable(Table):
    model = Service
    columns = [
        {'field': 'status',         'permission': 'view',       'styles': ['narrow', 'border-right']},
        {'field': 'host',           'permission': 'view'},
        {'field': 'protocol',       'permission': 'view'},
        {'field': 'port',           'permission': 'view'},
        {'field': 'uptime',         'permission': 'view',       'styles': ['narrow'],   'appended_text': '%'},
        {'field': 'enabled',        'permission': 'modify',     'action': 'toggle',     'styles': ['narrow', 'border-left']},
        {'common_action': 'passwd', 'permission': 'passwd'},
        {'common_action': 'check',  'permission': 'modify'},
        {'common_action': 'modify', 'permission': 'modify'},
        {'common_action': 'delete', 'permission': 'delete'},
    ]


