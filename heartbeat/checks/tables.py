from core.tables import Table
from .models import Check


class CheckTable(Table):
    model = Check
    columns = [
        {'field': 'status', 'styles': ['narrow']},
        {'field': 'host', 'styles': ['border-right']},
        {'field': 'timestamp', 'datetime': 'past'},
        {'field': 'description'},
    ]