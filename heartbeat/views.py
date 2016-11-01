from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from heartbeat.teams.models import Team
from heartbeat.checks.models import Check
from heartbeat.checks.tables import CheckTable
from heartbeat.schedule.models import get_schedule

@login_required
def Index(request):
    checks = Check.objects.order_by('-timestamp')[:20]
    table = CheckTable(model=Check, elements=checks)
    table.build(request)
    data = {
        'teams': Team.objects.order_by('name'),
        'table': table,
        'schedule': get_schedule(),
    }
    return render(request, 'index.html', data)