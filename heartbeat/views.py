from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from heartbeat.teams.models import Team
from heartbeat.checks.models import Check
from heartbeat.checks.tables import CheckTable


@login_required
def Index(request):
    teams = Team.objects.order_by('name')
    checks = Check.objects.order_by('-timestamp')
    if len(checks) > 20:
        checks = checks[:20]
    table = CheckTable(model=Check, elements=checks)
    data = {'teams': teams, 'table': table.build(request)}
    return render(request, 'index.html', data)
