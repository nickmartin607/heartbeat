from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from authentication.decorators import *
from core.views import *
from .models import *
from .forms import *
from .tasks import *


@login_required
def Index(request):
    if request.user.is_staff:
        template = 'index_staff.html'
        data = {
            'host_checks': HostCheck.objects.order_by('-timestamp')[:10],
            'service_checks': ServiceCheck.objects.order_by('-timestamp')[:10],
            'config': get_config(),
        }
    else:
        template = 'index_teams.html'
        data = {
            'services': Service.objects.filter(visible=True),
            'injects': Inject.objects.filter(visible=True).filter(team=request.user.account.team),
        }
    data['teams'] = Team.objects.order_by('name')
    return render(request, template, data)

@has_permission('view', Host)
def SystemList(request):
    data = {
        'hosts': Host.objects.order_by('ip'),
    }
    return render(request, 'models/systems.html', data)

@has_permission('view', Inject)
def InjectList(request):
    data = {
        'active_injects': Inject.objects.filter(visible=True),
        'inactive_injects': Inject.objects.filter(visible=False).filter(completed=False),
        'completed_injects': Inject.objects.filter(completed=True),
    }
    return render(request, 'models/injects.html', data)

@has_permission('view', Task)
def TaskList(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.complete()
            return redirect('task:all')
    else:
        form = TaskForm()
    data = {
        'completed_tasks': Task.objects.filter(completed=True),
        'form': form,
    }
    return render(request, 'models/tasks.html', data)

def ServiceAdd(request, hid):
    host = get_object_or_404(Host, pk=hid)
    initial = {'host': host, 'team': host.team}
    return AddView(request, Service, ServiceForm, initial)

def SystemCheckAll(request):
    for host in Host.objects.filter(visible=True):
        host.execute_check()
    for service in Service.objects.filter(visible=True):
        service.execute_check()
    return redirect('system:all')
    
