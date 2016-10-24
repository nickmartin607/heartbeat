from django.shortcuts import render, redirect
from .decorators import *

@has_permission('access')
def ListView(request, model, table):
    try:
        table.sort(request.GET.get('order_by'))
    except:
        pass
    data = {'table': table.build(request)}
    return render(request, 'table.html', data)
    
    
@has_permission('access')
def DetailView(request, model, model_form, id):
    try:
        instance = model.objects.get(pk=id)
    except:
        return redirect('404')
    if instance.enabled or request.user.is_staff:
        form = model_form(instance=instance)
        data = {'form': form}
        return render(request, 'form.html', data)
    else:
        return redirect('401')
    
    
@has_permission('create')
def CreateView(request, model, model_form):
    next_url = model._url('create')
    if request.method == 'POST':
        form = model_form(request.POST, next_url=next_url)
        if form.is_valid():
            instance = form.save()
            return redirect(model._namespace('all'))
    else:
        form = model_form(next_url=next_url)
    data = {'form': form}
    return render(request, 'form.html', data)


@has_permission('modify')
def ModifyView(request, model, model_form, id):
    try:
        instance = model.objects.get(pk=id)
    except:
        return redirect('404')
    next_url = model._url('modify', args=[id])
    if request.method == 'POST':
        form = model_form(request.POST, instance=instance, next_url=next_url)
        if form.is_valid():
            instance = form.save()
            return redirect(model._namespace('all'))
    else:
        form = model_form(instance=instance, next_url=next_url)
    data = {'id': id, 'instance': instance, 'form': form}
    return render(request, 'form.html', data)


@has_permission('delete')
def DeleteView(request, model, id):
    try:
        instance = model.objects.get(pk=id)
    except:
        return redirect('404')
    instance.delete()
    return redirect(model._namespace('all'))
    

@has_permission('modify')
def ToggleView(request, model, id):
    try:
        instance = model.objects.get(pk=id)
    except:
        return redirect('404')
    instance.toggle()
    return redirect(model._namespace('all'))
