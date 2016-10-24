from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from .forms import LoginForm, PasswdForm

def Login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    data = {'form': form, 'next_url': reverse('login')}
    return render(request, 'login.html', data)

def Logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

@login_required
def Passwd(request):
    if request.method == 'POST':
        user = request.user
        form = PasswdForm(data=request.POST, user=user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('index')
    else:
        form = PasswdForm(request.user)
    data = {'title': "Change our Password", 'form': form, 'next_url': reverse('passwd')}
    return render(request, 'form.html', data)

def Error401(request):
    return render(request, 'error401.html')

def Error404(request):
    return render(request, 'error404.html')