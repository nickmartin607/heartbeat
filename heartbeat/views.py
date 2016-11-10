from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from authentication.decorators import *
from core.views import AddView, ModifyView, DeleteView, ToggleView
from .models import *


################################################################################
# Homepage
################################################################################
@login_required
def Index(request):
    data = {
        'teams': Team.objects.order_by('name'),
        'checks': Check.objects.order_by('-timestamp')[:20],
        'schedule': get_schedule(),
        'injects': Inject.objects.filter(visible=True).filter(team=request.user.account.team),
        'services': Service.objects.filter(visible=True).order_by('last_checked'),
    }
    template = 'index_staff.html' if request.user.is_staff else 'index_teams.html'
    return render(request, template, data)
################################################################################
# Listings
################################################################################
@has_permission('view', Host)
def SystemList(request):
    return render(request, 'systems.html', {'hosts': Host.objects.order_by('ip')})
@has_permission('view', Inject)
def InjectList(request):
    data = {
        'active_injects': Inject.objects.filter(visible=True),
        'inactive_injects': Inject.objects.filter(visible=False).filter(status=False),
        'completed_injects': Inject.objects.filter(status=True),
    }
    return render(request, 'injects.html', data)
################################################################################
# Create
################################################################################
def HostAdd(request):
    return AddView(request, Host, HostForm)
def ServiceAdd(request, hid):
    try:
        initial = {'host': Host.objects.get(pk=hid)}
    except:
        initial = {}
    return AddView(request, Service, ServiceForm, initial)
def InjectAdd(request):
    return AddView(request, Inject, InjectForm)
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
# Toggles
################################################################################
def HostToggle(request, id):
    return ToggleView(request, Host, id, 'system:all')
def ServiceToggle(request, id):
    return ToggleView(request, Service, id, 'system:all')
def InjectToggle(request, id):
    return ToggleView(request, Inject, id, 'inject:all')
################################################################################
# Miscellaneous
################################################################################
@has_permission('modify', Schedule)
def ScheduleToggle(request):
    schedule = get_schedule()
    schedule.toggle()
    return redirect('index')
@has_permission('modify', Host)
def HostCheck(request, id):
    try:
        instance = Host.objects.get(pk=id)
    except:
        return redirect('404')
    instance.do_check()
    return redirect('system:all')
@has_permission('modify', Service)
def ServiceCheck(request, id):
    try:
        instance = Service.objects.get(pk=id)
    except:
        return redirect('404')
    instance.do_check()
    return redirect('system:all')
    
@has_permission('modify', Inject)
def InjectComplete(request, id):
    try:
        instance = Inject.objects.get(pk=id)
    except:
        return redirect('404')
    instance.complete()
    return redirect('inject:all')