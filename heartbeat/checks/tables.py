from core.tables import Table
from .models import Check


class CheckTable(Table):
    model = Check
    columns = [
        {'field': 'status',         'permission': 'view',       'styles': ['narrow']},
        {'field': 'host',           'permission': 'view',       'styles': ['border-right']},
        {'field': 'timestamp',      'permission': 'view',       'datetime': 'past'},
        {'field': 'description',    'permission': 'view'},
    ]