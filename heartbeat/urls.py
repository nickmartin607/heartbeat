from django.conf.urls import url, include
from django.contrib import admin
from authentication import urls as auth_urls
from .models import Host, Service, Inject
from .forms import HostForm, ServiceForm, InjectForm
from .views import Index, SystemList, SystemCheckAll, ServiceAdd, InjectList, TaskList
from core.views import AddView, ModifyView, DeleteView, ToggleView, CheckView, CompleteView

system_urls = [
    url(r'^$',                          SystemList,                                                                 name='all'),
    url(r'^check/all',                  SystemCheckAll,                                                             name='check-all'),
]
host_urls = [
    url(r'^add$',                       AddView,        kwargs={'model': Host, 'model_form': HostForm},             name='add'),
    url(r'^modify/(?P<id>[0-9]+)$',     ModifyView,     kwargs={'model': Host, 'model_form': HostForm},             name='modify'),
    url(r'^delete/(?P<id>[0-9]+)$',     DeleteView,     kwargs={'model': Host, 'redirect_url': 'system:all'},       name='delete'),
    url(r'^toggle/(?P<id>[0-9]+)$',     ToggleView,     kwargs={'model': Host, 'redirect_url': 'system:all'},       name='toggle'),
    url(r'^check/(?P<id>[0-9]+)$',      CheckView,      kwargs={'model': Host, 'redirect_url': 'system:all'},       name='check'),
]
service_urls = [
    url(r'^add/(?P<hid>[0-9]+)$',       ServiceAdd,                                                                 name='add'),
    url(r'^modify/(?P<id>[0-9]+)$',     ModifyView,     kwargs={'model': Service, 'model_form': ServiceForm},       name='modify'),
    url(r'^delete/(?P<id>[0-9]+)$',     DeleteView,     kwargs={'model': Service, 'redirect_url': 'system:all'},    name='delete'),
    url(r'^toggle/(?P<id>[0-9]+)$',     ToggleView,     kwargs={'model': Service, 'redirect_url': 'system:all'},    name='toggle'),
    url(r'^check/(?P<id>[0-9]+)$',      CheckView,      kwargs={'model': Service, 'redirect_url': 'system:all'},    name='check'),
]
inject_urls = [
    url(r'^$',                          InjectList,                                                                 name='all'),
    url(r'^add$',                       AddView,        kwargs={'model': Inject, 'model_form': InjectForm},         name='add'),
    url(r'^modify/(?P<id>[0-9]+)$',     ModifyView,     kwargs={'model': Inject, 'model_form': InjectForm},         name='modify'),
    url(r'^delete/(?P<id>[0-9]+)$',     DeleteView,     kwargs={'model': Inject},                                   name='delete'),
    url(r'^toggle/(?P<id>[0-9]+)$',     ToggleView,     kwargs={'model': Inject},                                   name='toggle'),
    url(r'complete/(?P<id>[0-9]+)$',    CompleteView,   kwargs={'model': Inject},                                   name='complete'),
]
task_urls = [
    url(r'^$',                          TaskList,                                                                   name='all'),
]
    
urlpatterns = [
    url(r'^$',                          Index,                                                                      name='index'),
    url(r'^systems/',                   include(system_urls,                                                        namespace='system')),
    url(r'^hosts/',                     include(host_urls,                                                          namespace='host')),
    url(r'^services/',                  include(service_urls,                                                       namespace='service')),
    url(r'^tasks/',                     include(task_urls,                                                          namespace='task')),
    url(r'^injects/',                   include(inject_urls,                                                        namespace='inject')),
    url(r'^',                           include(auth_urls)),
    url(r'^admin/',                     include(admin.site.urls)),
]