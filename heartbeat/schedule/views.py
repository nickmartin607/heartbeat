from django.shortcuts import redirect
from django.http import HttpResponse
from core.authentication.decorators import has_permission
from .models import *

def Toggle(request, state):
    sched = get_schedule()
    sched.toggle(state)
    return redirect('index')
