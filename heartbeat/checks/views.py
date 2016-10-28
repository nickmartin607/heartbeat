from core.views import ListView
from .models import Check
from .tables import CheckTable


def CheckList(request):
    elements = Check.objects.order_by('-last_checked')[:30]
    table = CheckTable(model=Check, name="Last 30 Checks", elements=elements)
    return ListView(request, Check, table)
