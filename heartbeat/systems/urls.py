from django.conf.urls import url, include
from core.views import *
from .models import Host, Service
from .forms import HostForm, ServiceForm
from .views import *


host_urls = [
    url(r'^$',                          HostList,                                                               name='all'),
    url(r'^create$',                    CreateView,             {'model': Host, 'model_form': HostForm},        name='create'),
    url(r'^modify/(?P<id>[0-9]+)$',     ModifyView,             {'model': Host, 'model_form': HostForm},        name='modify'),
    url(r'^delete/(?P<id>[0-9]+)$',     DeleteView,             {'model': Host},                                name='delete'),
    url(r'^check/(?P<id>[0-9]+)$',      HostCheck,                                                              name='check'),
    url(r'^toggle/(?P<id>[0-9]+)$',     ToggleView,             {'model': Host},                                name='toggle'),
]

service_urls = [
    url(r'^$',                          ServiceList,                                                            name='all'),
    url(r'^create$',                    CreateView,             {'model': Service, 'model_form': ServiceForm},  name='create'),
    url(r'^modify/(?P<id>[0-9]+)$',     ModifyView,             {'model': Service, 'model_form': ServiceForm},  name='modify'),
    url(r'^delete/(?P<id>[0-9]+)$',     DeleteView,             {'model': Service},                             name='delete'),
    url(r'^check/(?P<id>[0-9]+)$',      ServiceCheck,                                                           name='check'),
    url(r'^toggle/(?P<id>[0-9]+)$',     ToggleView,             {'model': Service},                             name='toggle'),
    url(r'^passwd/(?P<id>[0-9]+)$',     ServicePasswd,                                                          name='passwd'),
]

urlpatterns = [
    url(r'^hosts/',                     include(host_urls,                                                      namespace='host')),
    url(r'^services/',                  include(service_urls,                                                   namespace='service')),
]