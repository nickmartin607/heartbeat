from django.shortcuts import render, redirect
from core.authentication.decorators import has_permission
from .models import Team


@has_permission('modify', Team)
def PerformChecks(request, id):
    try:
        team = Team.objects.get(pk=id)
    except:
        return redirect('404')
    [h.do_check() for h in team.hosts.filter(enabled=True)]
    hosts = team.hosts.filter(enabled=True).filter(status=True)
    [s.do_check() for h in hosts for s in h.services.filter(enabled=True)]
    return redirect('index')


@has_permission('modify', Team)
def AdjustPoints(request, id, transaction, points):
    try:
        team = Team.objects.get(pk=id)
    except:
        return redirect('404')
    team.adjust_points(points, transaction)
    return redirect('index')
            