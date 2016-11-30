from django.shortcuts import render, redirect
from authentication.decorators import has_permission

@has_permission('add')
def AddView(request, model, model_form, initial={}):
    heading = 'Add a New {}'.format(model._meta.model_name.capitalize())
    if request.method == 'POST':
        form = model_form(request.POST)
        if form.is_valid():
            instance = form.save()
            return redirect(form.redirect_url)
    else:
        form = model_form(initial=initial)
    return render(request, 'form.html', {'form': form, 'heading': heading})

@has_permission('modify')
def ModifyView(request, model, model_form, id):
    heading = 'Modify the {}'.format(model._meta.model_name.capitalize())
    try:
        instance = model.objects.get(pk=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = model_form(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
            return redirect(form.redirect_url)
    else:
        form = model_form(instance=instance)
    data = {'id': id, 'instance': instance, 'form': form, 'heading': heading}
    return render(request, 'form.html', data)

@has_permission('delete')
def DeleteView(request, model, id, redirect_url):
    try:
        instance = model.objects.get(pk=id)
        instance.delete()
        return redirect(redirect_url)
    except:
        return redirect('404')

@has_permission('modify')
def ToggleView(request, model, id, redirect_url):
    try:
        instance = model.objects.get(pk=id)
    except:
        return redirect('404')
    instance.toggle()
    return redirect(redirect_url)
    
@has_permission('modify')
def CheckView(request, model, id, redirect_url):
    try:
        instance = model.objects.get(pk=id)
    except:
        return redirect('404')
    (result, details) = instance.execute_check()
    return redirect(redirect_url)
        
@has_permission('modify')
def CompleteView(request, model, id, redirect_url):
    try:
        instance = model.objects.get(pk=id)
    except:
        return redirect('404')
    instance.complete()
    return redirect(redirect_url)