from django.shortcuts import render, redirect, get_object_or_404
from authentication.decorators import has_permission

@has_permission('add')
def AddView(request, model, model_form, initial={}):
    if request.method == 'POST':
        form = model_form(request.POST)
        if form.is_valid():
            instance = form.save()
            return redirect(form.redirect_url)
    else:
        form = model_form(initial=initial)
    heading = 'Add a New {}'.format(model._meta.model_name.capitalize())
    return render(request, 'form.html', {'form': form, 'heading': heading})

@has_permission('modify')
def ModifyView(request, model, model_form, id):
    instance = get_object_or_404(model, pk=id)
    if request.method == 'POST':
        form = model_form(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
            return redirect(form.redirect_url)
    else:
        form = model_form(instance=instance)
    heading = 'Modify the {}'.format(model._meta.model_name.capitalize())
    data = {'id': id, 'instance': instance, 'form': form, 'heading': heading}
    return render(request, 'form.html', data)

@has_permission('delete')
def DeleteView(request, model, id, redirect_url=None):
    instance = get_object_or_404(model, pk=id)
    instance.delete()
    return redirect(redirect_url or '{}:all'.format(model.lower()))

@has_permission('modify')
def ToggleView(request, model, id, redirect_url=None):
    instance = get_object_or_404(model, pk=id)
    instance.toggle()
    return redirect(redirect_url or '{}:all'.format(model.lower()))
    
@has_permission('modify')
def CheckView(request, model, id, redirect_url=None):
    instance = get_object_or_404(model, pk=id)
    instance.execute_check()
    return redirect(redirect_url or '{}:all'.format(model.lower()))
        
@has_permission('modify')
def CompleteView(request, model, id, redirect_url=None):
    instance = get_object_or_404(model, pk=id)
    instance.complete()
    return redirect(redirect_url or '{}:all'.format(model.lower()))