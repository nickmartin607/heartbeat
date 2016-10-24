from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from heartbeat.teams.models import Team
from heartbeat.checks.models import Check
from heartbeat.checks.tables import CheckTable


@login_required
def Index(request):
    blue = Team.objects.get(pk=2)
    red = Team.objects.get(pk=3)
    checks = Check.objects.order_by('-timestamp')
    if len(checks) > 20:
        checks = checks[:20]
    table = CheckTable(model=Check, elements=checks)
    data = {'red_team': red, 'blue_team': blue, 'table': table.build(request)}
    return render(request, 'index.html', data)
