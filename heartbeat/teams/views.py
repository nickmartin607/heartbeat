from django.shortcuts import render, redirect
from core.decorators import has_permission
from heartbeat.systems.models import Host, Service
from .models import Team


@has_permission('modify', Team)
def PerformChecks(request, id):
    hosts = Host.objects.filter(team__pk=id).filter(enabled=True)
    [host.do_check() for host in hosts]
    services = Service.objects.filter(host__in=hosts).filter(enabled=True)
    [service.do_check() for service in services]
    return redirect('index')


@has_permission('modify', Team)
def AdjustPoints(request, id, transaction, points):
    try:
        team = Team.objects.get(pk=id)
    except:
        return redirect('404')
    team.adjust_points(points, transaction)
    return redirect('index')
            