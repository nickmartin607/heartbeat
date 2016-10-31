from django.shortcuts import render, redirect
from core.authentication.decorators import has_permission
from core.views import ListView
from heartbeat.teams.models import Team
from .models import Host, Service, Credential
from .forms import CredentialForm
from .tables import HostTable, ServiceTable


def HostList(request):
    elements = Host.objects.order_by('-status', '-enabled')
    table = HostTable(model=Host, name="All Hosts", elements=elements)
    return ListView(request, Host, table)
    
@has_permission('modify', Team)
def HostCheck(request, id):
    try:
        instance = Host.objects.get(pk=id)
    except:
        return redirect('404')
    instance.do_check()
    return redirect(Host.namespace('all'))

def ServiceList(request):
    services = Service.objects.order_by('-status', '-enabled')
    table = ServiceTable(model=Service, name="Services", elements=services)
    return ListView(request, Service, table)
    
@has_permission('modify', Team)
def ServiceCheck(request, id):
    try:
        instance = Service.objects.get(pk=id)
    except:
        return redirect('404')
    instance.do_check()
    return redirect(Service.namespace('all'))

@has_permission('modify', Credential)
def ServicePasswd(request, id):
    next_url = Service.url('passwd', args=[id])
    instance = Service.objects.get(pk=id)
    try:
        credential = Credential.objects.get(pk=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = CredentialForm(request.POST, instance=credential, next_url=next_url)
        new_password = str(request.POST.get('password')).strip()
        retype_password = str(request.POST.get('new_password')).strip()
        old_password = str(request.POST.get('old_password')).strip()
        if old_password == credential.password and retype_password == new_password:
            if form.is_valid():
                form.save()
                return redirect('index')
    else:
        form = CredentialForm(instance=credential, next_url=next_url)
    data = {'title': "Change {} Credentials".format(Service.modelname.capitalize()), 'form': form}
    return render(request, 'form.html', data)