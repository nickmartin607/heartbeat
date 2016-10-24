from django.conf.urls import url, include
from core.views import *
from .models import Inject
from .forms import InjectForm, InjectViewForm
from .views import InjectList, InjectComplete


inject_urls = [
    url(r'^$',                          InjectList,                                                                 name='all'),
    url(r'^view/(?P<id>[0-9]+)$',       DetailView,             {'model': Inject, 'model_form': InjectViewForm},    name='view'),
    url(r'^create$',                    CreateView,             {'model': Inject, 'model_form': InjectForm},        name='create'),
    url(r'^modify/(?P<id>[0-9]+)$',     ModifyView,             {'model': Inject, 'model_form': InjectForm},        name='modify'),
    url(r'^delete/(?P<id>[0-9]+)$',     DeleteView,             {'model': Inject},                                  name='delete'),
    url(r'^complete/(?P<id>[0-9]+)$',   InjectComplete,                                                             name='complete'),
    url(r'^toggle/(?P<id>[0-9]+)$',     ToggleView,             {'model': Inject},                                  name='toggle'),
]

action_urls = []

urlpatterns = [
    url(r'^injects/',                   include(inject_urls,                                                        namespace='inject')),
    url(r'^actions/',                   include(action_urls,                                                        namespace='action')),
]
