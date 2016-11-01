from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from heartbeat.teams.models import Team
from heartbeat.systems.models import Host
from heartbeat.checks.models import Check
from heartbeat.schedule.models import get_schedule

@login_required
def Index(request):
    data = {
        'teams': Team.objects.order_by('name'),
        'hosts': Host.objects.order_by('ip'),
        'checks': Check.objects.order_by('-timestamp')[:20],
        'schedule': get_schedule(),
    }
    return render(request, 'index.html', data)