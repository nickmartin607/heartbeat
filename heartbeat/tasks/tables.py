from core.tables import Table
from .models import Inject
        
        
class InjectTable(Table):
    model = Inject
    columns = [
        {'field': 'status', 'styles': ['narrow', 'border-right']},
        {'field': 'team', 'styles': ['border-right'], 'staff-only': True},
        {'field': 'subject', 'action': 'view'},
        {'field': 'point_value', 'action': 'complete', 'staff-only-action': True},
        {'field': 'deadline', 'datetime': 'future'},
        {'field': 'enabled', 'action': 'toggle', 'styles': ['border-left', 'narrow'], 'staff-only': True},
        {'action': 'modify', 'styles': ['narrow'], 'staff-only': True},
        {'action': 'delete', 'styles': ['narrow'], 'staff-only': True},
    ]