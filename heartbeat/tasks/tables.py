from core.tables import Table
from .models import Inject
        
        
class InjectTable(Table):
    model = Inject
    columns = [
        {'field': 'status',         'permission': 'view',   'styles': ['border-right']},
        {'field': 'team',           'permission': 'view',   'styles': ['border-right']},
        {'field': 'subject',        'permission': 'view',   'action': 'view'},
        {'field': 'point_value',    'permission': 'modify',   'action': 'complete'},
        {'field': 'deadline',       'permission': 'view',   'datetime': 'future'},
        {'field': 'enabled',        'permission': 'modify', 'action': 'toggle',         'styles': ['border-left']},
        {'common_action': 'modify', 'permission': 'modify'},
        {'common_action': 'delete', 'permission': 'delete'},
    ]