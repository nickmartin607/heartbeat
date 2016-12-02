from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from authentication.decorators import *
from core.views import *
from .models import *
from .forms import *
from .tasks import *

################################################################################
# Homepage
################################################################################
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
################################################################################
# Listings
################################################################################
@has_permission('view', Host)
def SystemList(request):
    return render(request, 'models/systems.html', {'hosts': Host.objects.order_by('ip')})

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
################################################################################
# Create
################################################################################
def HostAdd(request):
    return AddView(request, Host, HostForm)
def ServiceAdd(request, hid):
    host = get_object_or_404(Host, pk=hid)
    # try:
        # host = Host.objects.get(pk=hid)
    initial = {'host': host, 'team': host.team}
    return AddView(request, Service, ServiceForm, initial)
    # except:
        # return redirect('404')
def InjectAdd(request):
    return AddView(request, Inject, InjectForm)
def TaskAdd(request):
    return AddView(request, Task, TaskForm)
################################################################################
# Modify
################################################################################
def HostModify(request, id):
    return ModifyView(request, Host, HostForm, id)
def ServiceModify(request, id):
    return ModifyView(request, Service, ServiceForm, id)
def InjectModify(request, id):
    return ModifyView(request, Inject, InjectForm, id)
################################################################################
# Delete
################################################################################
def HostDelete(request, id):
    return DeleteView(request, Host, id, 'system:all')
def ServiceDelete(request, id):
    return DeleteView(request, Service, id, 'system:all')
def InjectDelete(request, id):
    return DeleteView(request, Inject, id, 'inject:all')
################################################################################
# Toggle
################################################################################
def HostToggle(request, id):
    return ToggleView(request, Host, id, 'system:all')
def ServiceToggle(request, id):
    return ToggleView(request, Service, id, 'system:all')
def InjectToggle(request, id):
    return ToggleView(request, Inject, id, 'inject:all')
################################################################################
# Check
################################################################################
def CheckHost(request, id):
    return CheckView(request, Host, id, 'system:all')
def CheckService(request, id):
    return CheckView(request, Service, id, 'system:all')
def CheckServices(request):
    for service in Service.objects.filter(visible=True):
        service.execute_check()
    return redirect('system:all')
    
################################################################################
# Complete
################################################################################
def CompleteInject(request, id):
    return CompleteView(request, Inject, id, 'inject:all')