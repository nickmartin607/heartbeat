from django.shortcuts import redirect
from core.decorators import has_permission
from core.views import ListView
from .models import Inject
from .tables import InjectTable


def InjectList(request):
    elements = Inject.objects.all()
    table = InjectTable(model=Inject, name="Injects", elements=elements)
    return ListView(request, Inject, table)


@has_permission('modify', Inject)
def InjectComplete(request, id):
    try:
        instance = Inject.objects.get(pk=id)
    except:
        return redirect('404')
    instance.complete()
    return redirect(Inject._namespace('all'))
        
    